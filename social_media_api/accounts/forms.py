# forms.py
import os
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import FileExtensionValidator
from django.core.files.storage import default_storage
from .models import CustomUser, UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']


'''ensure all images are at most 5kb in size'''


def validate_image_size(value):
    filesize = value.size
    megabyte_limit = 5.0
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError(f"Max file size is {megabyte_limit} MB")


class UpdateProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(validators=[validate_image_size, FileExtensionValidator(
        allowed_extensions=['jpg', 'jpeg', 'png'])])
    '''give the user the option to remove the profile picture'''
    remove_picture = forms.BooleanField(
        required=False, label='Remove Profile Picture')

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'remove_picture', 'bio',]

    def save(self, commit=True):
        profile = super().save(commit=False)
        #if user chooses to remove their profile pic, set to default
        if self.cleaned_data['remove_picture']:
            if profile.profile_picture == 'default.jpg':
                pass
            else:
                # delete old image file
                profile.profile_picture.delete(
                    save=False)
                profile.profile_picture = 'default.jpg'
                profile.save()

        if commit:
            profile.save()
        return profile

#
#
#
