
from django.urls import path

from .views import NotificationDeleteView, notification_view
urlpatterns = [
    path('notifications', notification_view, name='notifications'),
    path('notifications/<int:pk>/delete',
         NotificationDeleteView.as_view(), name='notification_delete')
]
