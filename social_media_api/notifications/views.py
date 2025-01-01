from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic import DeleteView

from .models import Notification


@login_required
def notification_view(request):
    notifications = Notification.objects.filter(recipient=request.user)
    print("IN NOTIFICATIONS VIEW, recipient?", notifications[0].recipient)
    return render(request, 'notifications/notifications.html', {'notifications': notifications})


@login_required
def mark_as_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.read = True
    notification.save()
    return redirect('notification_view')


@login_required()
def delete_notification(request, pk):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.delete()
    return redirect('notifications')


class NotificationDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    template_name = 'notifications/delete_confirm.html'
    success_url = reverse_lazy('notifications')
    model = Notification

    def dispatch(self, request, pk):
        if request.method == 'POST':
            # Delete the object if confirmed
            noti = Notification.objects.get(id=pk)
            if noti.recipient == request.user:
                noti.delete()
                return redirect(self.success_url)
            else:
                raise PermissionDenied()
        else:
            return render(request, self.template_name, {'pk': pk})
