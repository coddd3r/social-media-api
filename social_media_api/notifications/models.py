from django.dispatch import receiver
from posts.models import Post, Like
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.

User = settings.AUTH_USER_MODEL


class Notification(models.Model):
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='actions')
    verb = models.CharField(max_length=255)
    target_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True)
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')

    timestamp = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=Like)
def create_notification(sender, instance, created, **kwargs):
    if created:
        # Assuming the post model has a user field for the author
        post = instance.post
        actor = instance.user
        recipient = post.author
        Notification.objects.create(
            recipient=recipient, actor=actor,  target=post, verb='liked your post')


#
#
#
