from django.shortcuts import render
from rest_framework.response import Response
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status, serializers
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny,
    IsAuthenticatedOrReadOnly,
)

from .serializers import *

class AuthViewSet(GenericViewSet):
    permission_classes = [AllowAny]

    # def register(self, request):
    #     """
    #     Create New User Profile .
    #     """
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     validated_data = serializer.validated_data
    #
    #     try:
    #         instance = serializer.save()
    #
    #         # Send OTP code to user to be used to activate account
    #         verify.send(validated_data['telephone'])
    #         SmsModel.objects.create(user=instance["user"])
    #     except Exception:
    #         logger.exception("failed to save profile")
    #         raise error_codes.FAILED_INITIAL_USER
    #
    #     return Response({"id": instance["user"].id}, status=status.HTTP_201_CREATED)

    def login(self, request):
        """
        Login USER ViewSet.
        """
        serializer = self.get_serializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer_user = serializer.validated_data['user']
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)

        if user == serializer_user:
            if user is not None:
                if user.is_active:
                    # login(request, user)
                    token, created = Token.objects.get_or_create(user=user)
                else:
                    raise serializers.ValidationError(
                        {"detail": "This account is inactive."})
            else:
                raise serializers.ValidationError(
                    {"detail": "Invalid! Please try again."})

            user_profile = User.objects.get(id=user.id)
            content = {
                "id": str(user_profile.id),
                "name": str(user_profile.username),
            }
            return Response(content, status=status.HTTP_200_OK)
        return Response({"Invalid! Please try again."})

    def logout(self, request):
        """
        Logout USER ViewSet.
        """
        if self.request.user.is_authenticated:
            self.request.user.auth_token.delete()
            logout(request)
            content = {"success": "User logged out successfully."}
            return Response(content, status=status.HTTP_204_NO_CONTENT)
        return Response({"User": "Not Found"})

    def retrieve(self, request):
        """
        Retrieve USER ViewSet.
        """
        if self.request.user.is_authenticated:
            content = {
                "id": str(request.user.id),
                "name": str(request.user),
                # "auth": str(request.auth),
            }
            return Response(content)
        return Response({"User": "Not Found. Please login."})

    def get_serializer_class(self):
        """
        Users should receive the specific serializer to be used.
        """
        # if self.action == "register":
        #     return CreateProfileSerializer
        if self.action == "login":
            return UserSignInSerializer