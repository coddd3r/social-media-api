from django.db import models
# from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class CustomUser(AbstractUser):
    # bio = models.TextField(max_length=200)
    bio = models.TextField()
    # profile_picture = models.ImageField()
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
    first_name = models.CharField(max_length=50, default="no_first_name")
    last_name = models.CharField(max_length=50, default="no_last_name")
    profile_picture = models.ImageField(
        default='default.jpg', upload_to='profile_pics', width_field='image_width', height_field='image_height')
    bio = models.TextField(max_length=300, null=True)
    image_width = models.PositiveIntegerField(
        blank=True, null=True, default=60)
    image_height = models.PositiveIntegerField(
        blank=True, null=True, default=60)

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_model_type(self):
        return self.__class__.__name__

    # resize all images to a standard size
   # def save(self, *args, **kwargs):
   #     if self.profile_picture:
   #         print("\n\n in model save pic:", self.profile_picture)
   #         from PIL import Image
   #         import io
   #         from django.core.files.base import ContentFile

   #         img = Image.open(self.profile_picture)
   #         if img.width != 200 or img.height != 200:
   #             output = io.BytesIO()
   #             img.resize((200, 200), Image.Resampling.LANCZOS).save(
   #                 output, format='png', quality=95)
   #             output.seek(0)
   #             self.profile_picture.save(
   #                 self.profile_picture.name, ContentFile(output.read()), save=False)
   #     super().save(*args, **kwargs)


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(user=instance)
        user_profile.save()

    def get_model_type(self):
        return self.__class__.__name__


#
