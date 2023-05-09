import logging

from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status, serializers
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny,
    IsAuthenticatedOrReadOnly,
)
from drf_spectacular.utils import extend_schema
from django.core.exceptions import ObjectDoesNotExist

from .models import *
from .serializers import *
from . import verify


# class SmsViewSet(GenericViewSet):
#     permission_classes = [IsAuthenticated]

#     def get_verification_code(self, request):
#         user = User.objects.get(user=request.user)
#         try:
#             verify.send(user.telephone)
#         except Exception as e:
#             raise serializers.ValidationError("Wrong number")

#         return Response({}, status=status.HTTP_201_CREATED)

#     def verify_authorization_code(self, request, *args, **kwargs):
#         serializer = SmsModelSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = User.objects.get(user=request.user)
#         user_sms = SmsModel.objects.get(user=user)
#         code = serializer.validated_data.get('code')

#         try:
#             if verify.check(user.telephone, code):
#                 user_sms.isVerified = True
#                 user_sms.counter += 1
#                 user_sms.save()

#         except Exception:
#             raise serializers.ValidationError("Invalid. Please try again.")

#         return Response({"success": "true"}, status=status.HTTP_200_OK)