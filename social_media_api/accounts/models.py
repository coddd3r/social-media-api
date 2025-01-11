from django.db import models
# from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class CustomUser(AbstractUser):
    followers = models.ManyToManyField(
        'self', symmetrical=False, related_name='follower_users')
    following = models.ManyToManyField(
        'self', symmetrical=False, related_name='following_users')

    email = models.EmailField(unique=True)

    def get_model_type(self):
        return self.__class__.__name__


class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='profile')
    # TODO!: consider using a handle vs username
    # first_name = models.CharField(max_length=50, default="no_first_name")
    # last_name = models.CharField(max_length=50, default="no_last_name")
    profile_picture = models.ImageField(
        default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(max_length=300, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_model_type(self):
        return self.__class__.__name__


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(user=instance)
        user_profile.save()

    def get_model_type(self):
        return self.__class__.__name__


#
