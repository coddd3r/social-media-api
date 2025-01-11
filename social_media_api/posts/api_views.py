from django_filters.rest_framework.filters import DateFilter
from django_filters.rest_framework.filterset import FilterSet

from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from .models import Post, Like
from .serializers import LikeSerializer, PostSerializer, PostUpdateSerializer


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


'''search for posts by keyword in content or title'''


class PostSearchView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'content']


'''custom filter for posts within a certain timerange'''


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


'''create post and add request user as the author'''


class PostCreate(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        if serializer.is_valid():
            # Add the author to the post before saving
            serializer.validated_data['author'] = self.request.user
            serializer.save()


'''view post details'''


class PostDetail(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


'''modify posts by owners users'''


class PostUpdate(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_update(self, serializer):
        if serializer.is_valid():
            """user and post author have to be the same"""
            if self.request.user == self.get_object().author:
                serializer.save()
            else:
                raise ValidationError(
                    'You are not authorized to delete this post')

    def get_object(self):
        pk = self.kwargs['pk']
        return generics.get_object_or_404(Post, id=pk)


"""delete posts"""


class PostDelete(generics.DestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        """user and post author have to be the same"""
        if self.request.user == instance.author:
            self.perform_destroy(instance)
        else:
            return Response("You are not authorized to delete this post", status=status.HTTP_403_FORBIDDEN)
        return Response("Post deleted successfully", status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        pk = self.kwargs['pk']
        return generics.get_object_or_404(Post, id=pk)


"""like and unlike posts"""


class LikeUnlikeView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        user = self.request.user
        post_id = self.kwargs['pk']
        post = Post.objects.get(id=post_id)
        # if already liked then unlike
        if Like.objects.filter(user=user, post=post).exists():
            Like.objects.filter(user=user, post=post).delete()
        else:
            serializer.save(user=user, post=post)


class PostListByTag(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        tag_name = self.kwargs['tag']
        return Post.objects.filter(tags__name__in=[tag_name])
#
