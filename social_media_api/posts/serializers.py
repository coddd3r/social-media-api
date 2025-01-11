from rest_framework import serializers

from .models import Post, Comment, Like
from accounts.serializers import CustomUserSerializer, BaseUserSmallSerializer  # type: ignore
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)

# use methods for likes and taggit's searlizer for tags


class PostSerializer(serializers.ModelSerializer):
    author = BaseUserSmallSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = '__all__'
        extra_fields = ['likes_count']

        read_only_fields = ['author']

    def get_likes_count(self, obj):
        return obj.likes.count()

    ''' return only user id for post likes since we already know the post '''

    def get_likes(self, obj):
        return [post.id for post in obj.likes.all()]


class PostUpdateSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Post
        # Only these fields can be updated
        fields = ['title', 'content', 'tags']
        extra_kwargs = {
            'id': {'read_only': True},
        }


class CommentSerializer(serializers.ModelSerializer):
    # nested serializer for the related Post
    post = PostSerializer(read_only=True)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data['user']
        post = validated_data['post']

        existing_instance = Like.objects.filter(post=post, user=user).first()
        # if post already liked
        if existing_instance:
            return existing_instance
        return super().create(validated_data)
