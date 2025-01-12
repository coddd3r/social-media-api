from django.core.paginator import EmptyPage, PageNotAnInteger
from django.views.generic.list import Paginator
from .forms import CommentForm, DateForm
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
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from accounts.models import CustomUser


from .forms import PostForm
from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment, Like

'''show all posts by all users in chronological order with latest first'''


class PostListView(ListView):
    model = Post
    paginate_by = 10  # Set the number of items per page
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        posts = Post.objects.all().order_by('-created_at')
        posts = PostSerializer(posts, many=True).data
        return posts


'''show the recent posts by all users the current user follows'''


class PostFeedView(ListView):
    model = Post
    paginate_by = 10  # Set the number of items per page
    template_name = 'posts/post_feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        request = self.request
        following_users = request.user.following.all()
        # order posts with most recent first
        posts = Post.objects.filter(
            author__in=following_users).order_by('-created_at')
        posts = PostSerializer(posts, many=True).data
        return posts


class PostCreateView(CreateView, LoginRequiredMixin):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_create.html'

    def form_valid(self, form):
        author = CustomUser.objects.get(id=self.request.user.pk)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = PostSerializer(self.get_object()).data
        context["comments"] = Comment.objects.filter(
            post=self.get_object())[:10]
        return context


class PostDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    template_name = 'posts/post_delete.html'
    success_url = reverse_lazy('posts')
    model = Post

    def dispatch(self, request, pk):
        if request.method == 'POST':
            # Delete the object if confirmed
            post = Post.objects.get(id=pk)
            # make sure requester is the author of the post
            if post.author == request.user:
                post.delete()
                return redirect(self.success_url)
            else:
                raise PermissionDenied()
        else:
            return render(request, self.template_name, {'object': PostSerializer(self.get_object())})


'''search for posts with keyword in either title or content'''


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


'''search for posts that were created between start and end date provided'''


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


@login_required
def like_post(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(
            user=request.user, post=post)
        if created:
            post.likes.add(request.user)
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
        posts = Post.objects.filter(tags__name=tag)
        return render(request, 'posts/tagged_posts.html', {'posts': posts, 'tag': tag})


##
# COMMENTS SECTION
##


class CommentPagination(PageNumberPagination):
    # max comments per page
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class CommentListView(ListView):
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


class CommentCreateView(CreateView, LoginRequiredMixin, UserPassesTestMixin):
    template_name = 'posts/comment_create.html'
    model = Comment
    form_class = CommentForm

    '''add author and post to comment'''

    def form_valid(self, form):
        author = get_object_or_404(CustomUser, pk=self.request.user.pk)
        form.instance.author = author
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={"pk": self.object.post.pk})


class CommentUpdateView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Comment
    form_class = CommentForm
    template_name = 'posts/comment_create.html'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={"pk": self.object.post.id})


class CommentDetailView(DetailView):
    def get(self, request):
        comment = Comment.objects.get(id=request.data['id'])
        serializer = CommentSerializer(comment)
        return Response(serializer.data)


class CommentDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    template_name = 'posts/comment_delete.html'
    model = Comment

    def dispatch(self, request, pk):
        if request.method == 'POST':
            # Delete the object if confirmed
            comment = get_object_or_404(Comment, pk=pk)
            successurl = self.get_success_url()
            # ensure comment author is same as user calling delete
            if comment.author == request.user:
                comment.delete()
                return redirect(successurl)
            else:
                raise PermissionDenied()
        elif request.method == "GET":
            return render(request, self.template_name, {'object': self.get_object()})
        else:
            raise PermissionDenied()

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={"pk": self.get_object().post.id})
