from .forms import DateForm
from http.client import HTTPResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.db.models import Q
from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, CreateView, UpdateView, DetailView


from rest_framework import filters
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import CustomUser


from .forms import PostForm
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .models import Post, Comment, Like

from notifications.models import Notification


class PostPagination(PageNumberPagination):
    page_size = 10  # Adjust the page size as needed
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostListView(ListView):
    model = Post
    paginate_by = 10  # Set the number of items per page
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        ret = Post.objects.all()
        print("getting posts for base list", ret)
        return ret


class PostCreateView(CreateView, LoginRequiredMixin):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_create.html'

    def form_valid(self, form):
        author = CustomUser.objects.get(id=self.request.user.pk)
        # author = CustomUser.objects.get(id=self.request.user.id)
        form.instance.author = author
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={"pk": self.object.id})


class PostUpdateView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_create.html'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={"pk": self.object.id})


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'


class PostDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    template_name = 'posts/post_delete.html'
    success_url = reverse_lazy('posts')
    model = Post

    def dispatch(self, request, pk):
        if request.method == 'POST':
            # Delete the object if confirmed
            post = Post.objects.get(id=pk)
            if post.author == request.user:
                post.delete()
                return redirect(self.success_url)
            else:
                raise PermissionDenied()
        else:
            return render(request, self.template_name, {'object': PostSerializer(self.get_object())})


class PostSearchView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        search_term = self.request.GET.get('search_term')
        title_q = Q(title__icontains=search_term) if search_term else Q()
        content_q = Q(content__icontains=search_term) if search_term else Q()
        # combined_q = title_q & content_q
        results = Post.objects.filter(content_q | title_q)
        return results


def post_search(request):
    if request.method == "GET":
        search_term = request.GET.get('search_term')
        title_q = Q(title__icontains=search_term) if search_term else Q()
        content_q = Q(content__icontains=search_term) if search_term else Q()
        # combined_q = title_q & content_q
        results = Post.objects.filter(content_q | title_q)
        prompt = f"Post with the term:'{search_term}'"
        return render(request, 'posts/search_results.html', {'results': results, 'search_prompt': prompt})
    else:
        raise PermissionDenied()


def range_search_view(request):
    if request.method == 'POST':
        form = DateForm(request.POST)
        objects = []
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            objects = Post.objects.filter(
                created_at__range=(start_date, end_date))
            time_range = f"posts for time range{start_date} to {end_date}"
            return render(request, 'posts/search_results.html', {'results': objects, 'search_prompt': time_range})
        else:
            return render(request, 'posts/date_search.html', {'form': form})
    else:
        form = DateForm()
        return render(request, 'posts/date_search.html', {'form': form})


def feed_view(request):
    following_users = request.user.following.all()
    posts = Post.objects.filter(
        author__in=following_users).order_by('-created_at')
    posts = PostSerializer(posts, many=True).data

    context = {}
    context['posts'] = posts
    context['user'] = request.user
    return render(request, 'posts/post_feed.html', context)


@login_required
def like_post(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(
            user=request.user, post=post)
        if created:
            post.likes.add(request.user)
        print("like created", like)
        return redirect('post_detail', pk=pk)
    else:
        raise PermissionDenied


@login_required
def unlike_post(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(user=request.user, post=post).first()
        if like:
            post.likes.remove(request.user)
            like.delete()
        return redirect('post_detail', pk=pk)
    else:
        raise PermissionDenied


class TaggedPostListView(ListView):
    template_name = 'posts/tagged_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag_name = self.kwargs['tag']
        return Post.objects.filter(tags__name=tag_name)


def posts_tagged_by(request, tag):
    if request.method == "GET":
        tag_name = tag
        posts = Post.objects.filter(tags__name=tag_name)
        return render(request, 'posts/tagged_posts.html', {'posts': posts, 'tag': tag_name})
# @receiver(post_save, sender=Like)
# def send_like_notification(sender, instance, **kwargs):
#    liker = instance.user
#    post = instance.post
#
#    # Create a notification
#    Notification.objects.create(
#        user=liker,  # recipient
#        # notification message
#        message=f"{liker.username} liked your post: {post.title}",
#        link=post.get_absolute_url()  # link to the post
#    )


# @receiver(post_delete, sender=Like)
# def send_unlike_notification(sender, instance, **kwargs):
#     # Send a notification to the post author and/or other interested parties
#     pass

# "generics.get_object_or_404(Post, pk=pk)", "Like.objects.get_or_create(user=request.user, post=post)


##
# COMMENTS
##
class CommentPagination(PageNumberPagination):
    page_size = 20  # Adjust the page size as needed
    page_size_query_param = 'page_size'
    max_page_size = 100


class CommentListView(generics.ListAPIView):
    pagination_class = CommentPagination
    filter_backends = [filters.SearchFilter]

    def get(self, request):
        pk = self.kwargs['pk']
        post = Post.objects.get(id=pk)
        comments = Comment.objects.filter(post=post)
        paginated_comments = CommentPagination().paginate_queryset(
            queryset=comments, request=request)
        serializer = CommentSerializer(paginated_comments, many=True)
        return Response(serializer.data)


class CommentCreateView(APIView, LoginRequiredMixin, UserPassesTestMixin):
    serializer_class = CommentSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentUpdateView(APIView, LoginRequiredMixin, UserPassesTestMixin):
    def post(self, request):
        serializer = CommentSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            comment = Comment.objects.get(id=request.data['pk'])
            if request.user != request.user:
                raise PermissionDenied(
                    'Only the author can edit or delete this post')
            if comment.author == request.user:
                serializer.update(Comment, serializer.validated_data)
                return Response(serializer.data)
        return Response(serializer.errors, status=400)


class CommentDetailView(APIView):
    def get(self, request):
        # Handle GET request
        comment = Comment.objects.get(id=request.data['id'])
        serializer = CommentSerializer(comment)
        return Response(serializer.data)


class CommentDeleteView(generics.DestroyAPIView, LoginRequiredMixin, UserPassesTestMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def delete(self, request, pk):
        comment = self.get_object(pk)
        if request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
