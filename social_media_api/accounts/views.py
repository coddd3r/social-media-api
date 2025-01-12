from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse

from django.views.generic import View
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

# Create your views here.
from .forms import RegisterForm, UpdateUserForm, UpdateProfileForm
from .serializers import LoginSerializer
from .models import CustomUser, UserProfile
from posts.models import Post
from notifications.models import Notification


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("valid form for register")
            form.save()
            return redirect('login')

    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def profile_view(request, user_id):
    profile_instance = UserProfile.objects.get(id=user_id)
    user = CustomUser.objects.get(id=user_id)
    context = {}
    context['already_followed'] = user.followers.filter(
        id=request.user.id).count() > 0
    context['profile'] = profile_instance
    context['followers'] = user.followers.all()
    context['following'] = user.following.all()
    context['posts'] = list(Post.objects.filter(author=user))
    # context['posts'] = PostSerializer(Post.objects.filter(author=user))
    return render(request, "accounts/profile_view.html", context)


@login_required
def profile_update_view(request, user_id):
    '''ensure the editing user owns the profile'''
    if request.user.id != user_id:
        return HttpResponse(status=403, content='Forbidden')

    user_instance = CustomUser.objects.get(id=user_id)
    profile_instance = UserProfile.objects.get(id=user_id)

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=user_instance)
        profile_form = UpdateProfileForm(
            request.POST, request.FILES, instance=profile_instance)

        if user_form.is_valid() and profile_form.is_valid():
            profile_form.save()
            user_form.save()
            return redirect(reverse('profile', kwargs={'user_id': user_id}))
    else:
        user_form = UpdateUserForm(instance=user_instance)
        profile_form = UpdateProfileForm(instance=profile_instance)

    return render(request, 'accounts/profile_update.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(CustomUser, id=user_id)
    if not request.user.following.filter(id=user_id).exists():
        request.user.following.add(user_to_follow)
        # create notification on follow
        Notification.objects.create(
            recipient=user_to_follow, target=request.user, actor=request.user, verb="Followed you")
        user_to_follow.followers.add(request.user)
    return redirect(reverse_lazy('profile', kwargs={'user_id': user_id}))


@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
    request.user.following.remove(user_to_unfollow)
    user_to_unfollow.followers.remove(request.user)
    return redirect(reverse_lazy('profile', kwargs={'user_id': user_id}))


''' get a user's followers and who they follow '''


def get_connections(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    context = {}
    context['followers'] = user.followers.all()
    context['following'] = user.following.all()

    return render(request, 'accounts/connections_view.html', context)


'''enable deleting account'''


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('home')
    else:
        return render(request, 'accounts/delete_account.html')


'''users can ask for an auth token'''


class CustomAuthToken(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })
