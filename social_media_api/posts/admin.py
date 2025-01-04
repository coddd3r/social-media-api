from django.contrib import admin

from .models import Comment, Like, Post

# Register your models here.
admin.site.register([Post, Comment, Like])
