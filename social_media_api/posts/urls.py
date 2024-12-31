from django.urls import path

from .views import *

urlpatterns = [
    # path('posts/', PostListView.as_view({'get': 'list'}), name='posts'),
    path('', PostListView.as_view(), name='home'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('feed/', feed_view, name='feed'),
    path('post/new', PostCreateView.as_view(), name='create_post'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='update_post'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='delete_post'),
    path('post/range_search/', range_search_view, name='range_search'),
    path('post/search',
         post_search, name='search_post'),
    path('post/<int:pk>/comments/new/',
         CommentCreateView.as_view(), name='create_comment'),
    path('post/<int:pk>/comments/',
         CommentListView.as_view(), name='list_comment'),
    path('comment/<int:pk>/update/',
         CommentUpdateView.as_view(), name='update_comment'),
    path('comment/<int:pk>/delete/',
         CommentDeleteView.as_view(), name='delete_comment'),
    path('comment/<int:pk>/',
         CommentDetailView.as_view(), name='view_comment'),
    #     path('tags/<slug:tag_slug>/',
    #          PostByTagListView.as_view(), name='tag_posts'),
    path('post/<int:pk>/like/', like_post, name='like_post'),
    path('post/<int:pk>/unlike/', unlike_post, name='unlike_post'),
]
