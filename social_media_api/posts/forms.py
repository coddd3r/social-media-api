from django import forms
from .models import Post

from django.forms.widgets import SelectDateWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


class DateForm(forms.Form):
    start_date = forms.DateField(widget=SelectDateWidget)
    end_date = forms.DateField(widget=SelectDateWidget)
