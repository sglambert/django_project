from django.urls import path
from .views import (PostListView, PostDetailView, PostCreateView, PostUpdateView,
                    PostDeleteView, UserPostListView, PostDetail)
from . import views
from .api import api_like, api_comment


""" 
First arg of path() should be empty for home page
Second arg call the class / function view from views.py
Third arg specify the name of the url pattern
pk=primary key
"""

urlpatterns = [
    path('', PostListView.as_view(), name="blog-home"),
    path('user/<str:username>/', UserPostListView.as_view(), name="user-posts"),
    path('tags/<slug:tag_slug>/', views.TagIndexView.as_view(), name='posts_by_tag'),

    path('post/<int:pk>/', PostDetailView.as_view(), name="post-detail"),
    path('post/new/', PostCreateView.as_view(), name="post-create"),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name="post-update"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="post-delete"),

    path('about/', views.about, name="blog-about"),

    path('api/like/', api_like, name="api_like"),
    path('api/comment', api_comment, name="api_comment"),

    path('search/', views.SearchPostList, name="post-search"),
]
