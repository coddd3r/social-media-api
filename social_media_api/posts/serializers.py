from rest_framework import serializers

from .models import Post, Comment, Like
from accounts.serializers import CustomUserSerializer, BaseUserSmallSerializer  # type: ignore


class PostSerializer(serializers.ModelSerializer):
    author = BaseUserSmallSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        fields = ['id', 'author', 'title',
                  'content', 'created_at', 'updated_at', 'likes', 'likes_count']

    def get_likes_count(self, obj):
        return obj.likes.count()

    # return only user id for post likes since we already know the post
    def get_likes(self, obj):
        return [post.id for post in obj.likes.all()]


class CommentSerializer(serializers.ModelSerializer):
    # nested serializer for the related BlogPost
    post = PostSerializer(read_only=True)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id', 'author', 'content',
                  'created_at', 'updated_at', 'post']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data['user']
        post = validated_data['post']

        existing_instance = Like.objects.filter(post=post, user=user).first()
        if existing_instance:
            return existing_instance  # return the existing instance
        return super().create(validated_data)
