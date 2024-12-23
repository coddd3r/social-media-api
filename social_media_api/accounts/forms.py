# forms.py
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import CustomUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
