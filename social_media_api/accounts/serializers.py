from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token
from rest_framework import serializers

from .models import CustomUser, UserProfile


class BaseUserSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']


class CustomUserSerializer(serializers.ModelSerializer):
    # profile_picture = serializers.ImageField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio',
                  'password', 'followers', 'following']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # user = CustomUser(**validated_data)
        # user.set_password(validated_data['password'])
        # user.save()
        user = get_user_model().objects.create_user(**validated_data)
        token, created = Token.objects.create(user=user)
        return {'user': user, 'token': token.key}

    def get_followers(self, obj):
        followers_queryset = obj.followers.all()
        return BaseUserSmallSerializer(followers_queryset, many=True).data

    def get_following(self, obj):
        followers_queryset = obj.following.all()
        return BaseUserSmallSerializer(followers_queryset, many=True).data


class LoginSerializer(serializers.Serializer):
    # username = serializers.CharField(max_length=255)
    username = serializers.CharField()
    password = serializers.CharField(max_length=255, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)
        if user:
            attrs['user'] = user
            return attrs
        raise serializers.ValidationError('Invalid credentials')


class UserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = UserProfile
        fields = ['user', 'profile_picture']
