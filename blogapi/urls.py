from django.urls import path
from .views import PostList, PostDetail, CommentList, PostCommentList, CommentDetails

app_name = 'blog_api'

urlpatterns = [
    path('post/', PostList.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetail.as_view(), name='post_details'),
    path('comment/', CommentList.as_view(), name='comment_list'),
    path('comment/<int:pk>/', CommentDetails.as_view(), name='comment_details'),
    path('post/<int:pk>/comments/', PostCommentList.as_view(), name='post_commentlist')
]