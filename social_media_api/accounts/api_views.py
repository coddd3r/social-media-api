from django.contrib.auth import logout
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from accounts.views import CustomAuthToken
from .serializers import CustomUserSerializer, LoginSerializer, LogoutSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class LogoutAPIView(generics.CreateAPIView):
    serializer_class = LogoutSerializer

    def post(self, request):
        print("user authenticated?", request.user.is_authenticated)
        print(request.user.auth_token)
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            logout(request)
            return Response({"success": "Successfully logged out."}, status=status.HTTP_200_OK)
        return Response("user not logged in")
