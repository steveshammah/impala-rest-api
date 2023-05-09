import logging

from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.http import Http404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework import status, serializers
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny,
    IsAuthenticatedOrReadOnly,
)
from django.conf import settings
from rest_framework.settings import api_settings
from rest_framework.exceptions import NotFound, ValidationError as ExceptValidationError
from drf_spectacular.utils import extend_schema
from django.core.exceptions import ObjectDoesNotExist

from .models import *
from teamplayer.models import Team, Player
from league.models import Fixture, FixtureResult
from messaging.models import *
from members.models import *
from store.models import *
from .serializers import *
from teamplayer.serializers import *
from league.serializers import *
from messaging.serializers import *
from members.serializers import *
from store.serializers import *


@api_view(['GET'])
def home(request):
    api_urls = {
        'ACTIONS': 'ENDPOINT',
        'Users - All': '/api/users/',
        'User - Single': '/api/user/<str:pk>',
        'Authors - All': '/api/authors/',
        'Author - Single': '/api/authors/<str:pk>',
        'Articles - All': '/api/articles/',
        'Article - Single': '/api/articles/<str:pk>/',
        'Create Article': '/api/article-create/',
        'Update Article': '/api/article-update/<str:pk>',
        'Delete Article': '/api/article-delete/<str:pk>',

    }
    return Response(api_urls)


# USERS ENDPOINTS
@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_users(request):
    users = User.objects.all()
    serializer = UsersSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_user(request, pk):
    try:
        user = User.objects.get(id=pk)
        serializer = UsersSerializer(user, many=False)
        return Response(serializer.data)

    except Exception:
        return Response(f'User with id {pk} not found')


# AUTHORS ENDPOINTS
@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_authors(request):
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_author(request, pk):
    try:
        author = Author.objects.get(id=pk)
        serializer = AuthorSerializer(author, many=False)
        return Response(serializer.data)
    except Exception:
        return Response(f'Author with id {pk} not found')


# ARTICLES ENDPOINTS
@api_view(['GET'])
def get_all_articles(request):
    # print('Getting all posts')
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_article(request, pk):
    try:
        article = Article.objects.get(id=pk)
        serializer = ArticleSerializer(article, many=False)
        return Response(serializer.data)
    except Exception:
        return Response(f'Article with ID : {pk} Not Found')


@api_view(['POST'])
def create_article(request):
    # article = Articles.objects.get(id=pk)
    # print('Article Create', request.data)
    serializer = ArticleSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
    else:
        print('Form is not valid')
    return Response(serializer.data)


@api_view(['POST'])
def update_article(request, pk):
    article = Article.objects.get(id=pk)
    serializer = ArticleSerializer(instance=article, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_article(request, pk):
    article = Article.objects.get(id=pk)
    article.delete()
    return Response('Article delete successfully')


# PLAYERS ENDPOINTS
@api_view(['GET'])
def get_all_players(request):
    players = Player.objects.all()
    serializer = PlayerSerializer(players, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_player(request, pk):
    try:
        player = Player.objects.get(id=pk)
        serializer = PlayerSerializer(player, many=False)
        return Response(serializer.data)
    except Exception as error:
        return Response(f'Player with id {pk} not found')


# PRODUCTS ENDPOINTS
@api_view(['GET'])
def get_all_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_product(request, pk):
    try:
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    except Exception as error:
        return Response(f'Product with id {pk} not found')


# ------******* CLASS-BASED VIEWS *******------- #


class AuthorViewSet(GenericViewSet):
    def create(self, request, *args, **kwargs):
        """
        Create author instance .
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            instance = serializer.save()
        except Exception:
            # logger.exception("failed to save author profile")
            raise serializers.ValidationError("Failed to save author profile")

        return Response({"id": instance["author"].id}, status=status.HTTP_201_CREATED)

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
        Retrieve an author instance.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        Update an author instance.
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
        Destroy an author instance.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        # if instance.user.is_active:
        #     user = User.objects.get(id=instance.user.id)
        #     user.is_active = False
        #     user.save()
        instance.delete()

    def get_queryset(self):
        if self.action == 'list':
            queryset = Author.objects.all()
        else:
            queryset = Author.objects.filter(
                pk=self.kwargs["lookup_value"])
        return queryset

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(),
                                pk=self.kwargs["lookup_value"])
        try:
            # author = Author.objects.get(user=self.request.user)
            # if int(author.id) == int(self.kwargs["lookup_value"]):
            #     self.check_object_permissions(self.request, obj)
            if self.request.user.is_authenticated:
                self.check_object_permissions(self.request, obj)
        except Exception:
            raise serializers.ValidationError('User not authorized')
        return obj

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "create":
            permission_classes = [IsAdminUser]
        elif self.action in ["list", "retrieve", "update", "partial_update"]:
            permission_classes = [IsAuthenticated or IsAdminUser]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Users should receive the specific serializer to be used.
        """
        if self.action == "create":
            return CreateAuthorSerializer
        elif self.action == "list":
            return ListAuthorSerializer
        elif self.action in ["update", "partial_update"]:
            return UpdateAuthorSerializer
        else:
            return AuthorSerializer


class ArticleViewSet(GenericViewSet):

    @extend_schema(
        description="Create a new Article",
        # responses={
        #     status.HTTP_201_CREATED: CreateArticleSerializer(),
        #     status.HTTP_400_BAD_REQUEST: "Invalid input data",
        # }
        responses={
            200: CreateArticleSerializer(),
            400: 'Bad Request',
            404: 'Not Found',
        }
    )
    def create(self, request, *args, **kwargs):
        """
        Create article instance .
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            instance = serializer.save()
        except Article.DoesNotExist:
            # logger.exception("failed to save author profile")
            # raise serializers.ValidationError(
            #     "Failed to save article instance")
            return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({"id": instance["article"].id, "article": instance["article"].headline}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    @extend_schema(
        description="List Articles",
        # responses={
        #     status.HTTP_200_OK: ListArticleSerializer(many=True),
        #     status.HTTP_401_UNAUTHORIZED: "Authentication credentials were not provided.",
        #     status.HTTP_404_NOT_FOUND: "List items not found.",

        # }
        responses={
            200: ListArticleSerializer(many=True),
            401: "Authentication credentials were not provided.",
            404: "List items not found."
        }
    )
    def list(self, request, *args, **kwargs):
        """
        List Articles.
        """
        try:
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

        # except ValidationError as e:
        #     raise ExceptValidationError(
        #         {"Auth credentials not provided."}, code=401)
        # except ObjectDoesNotExist as e:
        #     raise NotFound({"List items not found."}, code=404)
        except Exception as e:
            return Response({"Not Found"}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        description="Retrieve an Article by ID",
        responses={
            status.HTTP_200_OK: ArticleSerializer(),
            status.HTTP_404_NOT_FOUND: "Article not found",
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve an article instance.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        description="Update an Article by ID",
        request=UpdateArticleSerializer,
        responses={
            status.HTTP_200_OK: UpdateArticleSerializer(),
            status.HTTP_400_BAD_REQUEST: "Invalid input data",
            status.HTTP_404_NOT_FOUND: "Article not found",
        }
    )
    def update(self, request, *args, **kwargs):
        """
        Update an article instance.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_update(serializer)
        except Exception as e:
            # logger.exception("failed to update author profile")
            # raise serializers.ValidationError(
            #     'Update failed. Please try again.')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({"Success": "Update complete"}, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()

    @extend_schema(
        description="Partial update an article by ID",
        request=UpdateArticleSerializer,
        responses={
            status.HTTP_200_OK: UpdateArticleSerializer(),
            status.HTTP_400_BAD_REQUEST: "Invalid input data",
            status.HTTP_404_NOT_FOUND: "Article not found",
        }
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @extend_schema(
        description="Delete an Article by ID",
        responses={
            status.HTTP_204_NO_CONTENT: "Article deleted successfully",
            status.HTTP_404_NOT_FOUND: "Article not found",
        }
    )
    def destroy(self, request, *args, **kwargs):
        """
        Destroy an article instance.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def get_queryset(self):
        if self.action == 'list':
            queryset = Article.objects.all()
        else:
            queryset = Article.objects.filter(
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
            return CreateArticleSerializer
        elif self.action == "list":
            return ListArticleSerializer
        elif self.action in ["update", "partial_update"]:
            return UpdateArticleSerializer
        else:
            return ArticleSerializer
