from django import forms
from .models import Post, Comment

from django.forms.widgets import SelectDateWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']


class DateForm(forms.Form):
    start_date = forms.DateField(widget=SelectDateWidget)
    end_date = forms.DateField(widget=SelectDateWidget)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
