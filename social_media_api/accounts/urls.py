from django.urls import path, reverse_lazy
from .views import get_connections, profile_view, CustomAuthToken, follow_user, register, unfollow_user
from django. contrib.auth.views import LoginView, LogoutView
LoginView.template_name = 'accounts/login.html'
LogoutView.template_name = 'accounts/logout.html'
urlpatterns = [
    path('register/', register, name='register'),
    # path('login/', user_login, name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:user_id>/', profile_view, name='profile'),
    path('token/', CustomAuthToken.as_view(), name='token'),
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow_user'),
    path('followers<int:user_id>/', get_connections, name='connections')
]
