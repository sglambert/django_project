import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Comment


@csrf_exempt
def api_like(request):
    """
    This api function adds like/unlike by a user to the database
    and returns response containing
    1)request status
    2)like status
    3)number of likes on the post after refreshing it from database
    """
    jsonresponse = {'success': True}
    
    data = json.loads(request.body)
    user_id = data['userId']
    post_id = data['postId']

    post = Post.objects.get(id=post_id)
    user = User.objects.get(id=user_id)

    if user in post.likes.all():
        post.likes.remove(user)
        like_status = 0
    else:
        post.likes.add(user)
        like_status = 1

    count = post.likes.count()

    jsonresponse['like_status'] = like_status
    jsonresponse['count'] = count
    
    return JsonResponse(jsonresponse)


def api_comment(request):
    """ This API function takes comment, comment author and post
    stores it to database and returns updated list of comments 
    to reactively change the comments list using vue """
    data = json.loads(request.body)
    user_id = data['userId']
    post_id = data['postId']
    comment_text = data['comment']

    user = User.objects.get(id=user_id)
    post = Post.objects.get(id=post_id)

    Comment.objects.create(commentator=user, blog=post,
                           comment=comment_text)

    all_comments = post.comment_set.all().values()
    jsonresponse = {'success': True, 'all_comments': list(all_comments)}
    return JsonResponse(jsonresponse)
