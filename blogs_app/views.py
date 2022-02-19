from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from hitcount.views import HitCountDetailView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.template import RequestContext
from taggit.models import Tag

from taggit.models import Tag
from django.template.defaultfilters import slugify

def home(request):
    """
    We use context to pass information to the home.html template.
    """
    # context = {'posts': post.objects.all()}
    context = {'posts': Post.objects.all()}
    return render(request, 'blogs_app/home.html', context)


class PostListView(ListView):
    """
    model = what model to query
    """
    model = Post
    template_name = 'blogs_app/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blogs_app/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


def PostDetail(request, pk):
    post = Post.objects.get(id=pk)
    current_logged_in_user = request.user
    comments_list = Comment.objects.filter(blog=post).order_by('-date_added')
    post_likes = post.likes.count()
    post_num = pk

    if current_logged_in_user in post.likes.all():
        like_status = 'Unlike'
    else:
        like_status = 'Like'

    if request.method == 'GET':
        form = CommentForm()

    if request.method == 'POST':
        if 'comment_button' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.commentator = current_logged_in_user
                new_comment.blog = post
                new_comment.save()
                return redirect('post-detail', pk=post_num)

    context = {'post': post, 'comments_list': comments_list, 'post_likes': post_likes,
               'like_status': like_status, 'form': form}

    return render(request, 'blogs_app/post_detail.html', context)


class PostDetailView(HitCountDetailView):
    model = Post
    template_name = "blogs_app/post_detail.html"
    slug_field = "slug"
    count_hit = True

    form = CommentForm

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()

            return redirect(reverse("post-detail", kwargs={
                'pk': post.pk
            }))

    def get_context_data(self, **kwargs):
        post_comments_count = Comment.objects.all().filter(post=self.object.id).count()
        post_comments = Comment.objects.all().filter(post=self.object.id)
        context = super().get_context_data(**kwargs)
        context.update({
            'form': self.form,
            'post_comments': post_comments,
            'post_comments_count': post_comments_count

        })
        return context


def SearchPostList(request):
    """
    Capture queries from url.
    """
    search_string = request.GET.get('search')
    filtered_posts = Post.objects.filter(title__icontains=search_string)
    context = {'filtered_posts': filtered_posts, 'captured_string': search_string}
    return render(request, 'blogs_app/search_posts.html', context)


class TagMixin(object):
    def get_context_data(self, **kwargs):
        context = super(TagMixin, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context


class TagIndexView(TagMixin,ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs.get('tag_slug'))

"""
class PostCreateView(LoginRequiredMixin, CreateView):
    # Run form validation after setting post author.
    model = Post
    # fields = ['title', 'content']
    fields = ['title', 'content', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
"""

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "blogs_app/post_form.html"
    fields = ['title', 'content', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True

        else:
            return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    # Redirect to homepage url after successfully deleting the post
    success_url = '/'

    def test_func(self):
        """ 'UserPassesTestMixin' class requires this function to work """

        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


def about(request):
    return render(request, 'blogs_app/about.html', {'title': 'about'})
