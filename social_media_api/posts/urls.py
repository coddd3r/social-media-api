from django.urls import path

from .views import *
from . import api_views
urlpatterns = [
    # path('posts/', PostListView.as_view({'get': 'list'}), name='posts'),
    path('', PostListView.as_view(), name='home'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('feed/', PostFeedView.as_view(), name='feed'),
    path('posts/new', PostCreateView.as_view(), name='create_post'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/update/', PostUpdateView.as_view(), name='update_post'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='delete_post'),
    path('posts/range_search/', range_search_view, name='range_search'),
    path('posts/search',
         post_search, name='search_post'),
    path('posts/<int:pk>/like/', like_post, name='like_post'),
    path('posts/<int:pk>/unlike/', unlike_post, name='unlike_post'),
    path('posts/<int:pk>/unlike/', unlike_post, name='unlike_post'),
    # path('post/tag/<str:tag>/', TaggedPostListView.as_view(), name='tag_posts'),
    path('posts/tag/<str:tag>/', posts_tagged_by, name='tag_posts'),
    path('posts/<int:pk>/comments/new/',
         CommentCreateView.as_view(), name='create_comment'),
    path('posts/<int:pk>/comments/',
         CommentListView.as_view(), name='comment_list'),
    path('comment/<int:pk>/update/',
         CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/',
         CommentDeleteView.as_view(), name='comment_delete'),
    path('comment/<int:pk>/',
         CommentDetailView.as_view(), name='comment_detail'),
    #     path('tags/<slug:tag_slug>/',
    #          PostByTagListView.as_view(), name='tag_posts'),


    path('api/posts/', api_views.PostListView.as_view(), name='api_posts'),
    path('api/posts/feed/', api_views.PostFeedAPI.as_view(), name='api_feed'),
    path('api/posts/<int:pk>/', api_views.PostDetail.as_view(),
         name='api_post_detail'),
    path('api/posts/search/', api_views.PostSearchView.as_view(),
         name='api_post_search'),
    path('api/posts/range_search/',
         api_views.PostRangeView.as_view(), name='api_range_search'),
]
