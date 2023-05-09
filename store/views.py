import logging

from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.settings import api_settings
from drf_spectacular.utils import extend_schema

from .models import *
from .serializers import *


class ProductViewSet(GenericViewSet):
    def create(self, request, *args, **kwargs):
        """
        Create product instance .
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            instance = serializer.save()
        except Exception:
            # logger.exception("failed to save author profile")
            raise serializers.ValidationError(
                "Failed to save product instance")

        return Response({"id": instance["product"].id, "product": instance["product"].product_name}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def list(self, request, *args, **kwargs):
        """
        List a queryset.
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        content = {
            "data": serializer.data,
            "total": len(serializer.data)
        }
        return Response(content, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a product instance.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        Update a product instance.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_update(serializer)
        except Exception:
            # logger.exception("failed to update author profile")
            raise serializers.ValidationError(
                'Update failed. Please try again.')

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({"Success": "Update complete"}, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Destroy a product instance.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def get_queryset(self):
        if self.action == 'list':
            queryset = Product.objects.all()
        else:
            queryset = Product.objects.filter(
                pk=self.kwargs["lookup_value"])
        return queryset

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(),
                                pk=self.kwargs["lookup_value"])
        if self.request.user.is_authenticated:
            self.check_object_permissions(self.request, obj)
        else:
            raise serializers.ValidationError('User not authorized')
        return obj

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ["create", "destroy", "update", "partial_update"]:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Users should receive the specific serializer to be used.
        """
        if self.action == "create":
            return CreateProductSerializer
        elif self.action == "list":
            return ListProductSerializer
        elif self.action in ["update", "partial_update"]:
            return UpdateProductSerializer
        else:
            return ProductSerializer
