from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path("posts/", include("posts.urls")),
    # path('', PostListView.as_view()),
    path('', include('accounts.urls')),
    path('', include('posts.urls')),
]
