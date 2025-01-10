from datetime import datetime
from django_filters.rest_framework.filters import DateFilter
from django_filters.rest_framework.filterset import FilterSet
from rest_framework import generics
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer


from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostFeedAPI(generics.ListAPIView,):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        request = self.request
        following_users = request.user.following.all()
        posts = Post.objects.filter(
            author__in=following_users).order_by('-created_at')
        posts = PostSerializer(posts, many=True).data
        return posts


class PostDetail(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostSearchView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'content']


class PostDateFilter(FilterSet):
    start_date = DateFilter(field_name='created_at', lookup_expr='gte')
    end_date = DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Post
        fields = []


class PostRangeView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostDateFilter
