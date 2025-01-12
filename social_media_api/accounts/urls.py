from . import api_views
from django.urls import path, include
from .views import get_connections, profile_view, CustomAuthToken, follow_user, register, unfollow_user, profile_update_view, delete_account
from django. contrib.auth.views import LoginView, LogoutView
LoginView.template_name = 'accounts/login.html'
LogoutView.template_name = 'accounts/logout.html'

urlpatterns = [
     #ui/template endpoints
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:user_id>/', profile_view, name='profile'),
    path('profile_update/<int:user_id>/',
         profile_update_view, name='profile_update'),
    path('delete_account/', delete_account, name='delete_account'),
    path('token/', CustomAuthToken.as_view(), name='token'),
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow_user'),
    path('followers<int:user_id>/', get_connections, name='connections'),
   
     #api endpoints
    path('api/register/', api_views.RegisterView.as_view(), name='api_register'),
    path('api/login/', api_views.LoginAPIView.as_view(), name='api_login'),
    path('api/logout/', api_views.LogoutAPIView.as_view(), name='api_logout'),
    path('api/profile/<int:user_id>/',
         api_views.ProfileRetrieveAPIView.as_view(), name='api_profile'),
    path('api/profile_update/<int:user_id>/',
         api_views.ProfileUpdateAPIView.as_view(), name='api_profile_update'),
    path('api/delete_account/', api_views.ProfileDeleteView.as_view(),
         name='api_delete_account'),
    # path('api_token/', CustomAuthToken.as_view(), name='token'),
    path('api/follow/<int:user_id>/', api_views.follow_user, name='follow_user'),
    path('api/unfollow/<int:user_id>/',
         api_views.unfollow_user, name='unfollow_user'),
    # path('api_followers<int:user_id>/', get_connections, name='connections')
    # djoser login
    # path('api/auth/', include('djoser.urls'))
    # path('api/auth/', include('djoser.urls.authtoken')),
    # drf provided login, log`x`out views
    # path('api-auth/', include('rest_framework.urls')),
    ##
]
