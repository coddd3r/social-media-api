from django.db import models
from django.conf import settings

from taggit.managers import TaggableManager

from accounts.models import CustomUser  # type: ignore


class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    # content = models.TextField()
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(CustomUser, related_name='post_likes')
    tags = TaggableManager()

    class Meta:
        ordering = ['created_at']  # Order posts by creation date
        verbose_name = 'Social Media Post'
        verbose_name_plural = 'Social Media Posts'

    def get_model_type(self):
        return self.__class__.__name__


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(CustomUser, related_name='comment_likes')

    class Meta:
        ordering = ['created_at']

    def get_model_type(self):
        return self.__class__.__name__


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['post', 'user']

    def get_model_type(self):
        return self.__class__.__name__
