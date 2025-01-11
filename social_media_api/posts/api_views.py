from django_filters.rest_framework.filters import DateFilter
from django_filters.rest_framework.filterset import FilterSet

from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer


from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions

''' view all posts'''


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


'''user specific list for posts by users they follow'''


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


'''search for posts by keyword in content or title'''


class PostSearchView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'content']


'''custom filter for posts within a certin timerange'''


class PostDateFilter(FilterSet):
    start_date = DateFilter(field_name='created_at', lookup_expr='gte')
    end_date = DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Post
        fields = []


'''provide user with all posts between a start date and end date'''


class PostRangeView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostDateFilter


'''modify posts by owners users'''


class UpdatePostView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
