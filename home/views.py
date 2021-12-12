from django.shortcuts import render
from .models import Articles
# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ArticleSerializer, UsersSerializer
# from django.http import JsonResponse
from django.contrib.auth.models import User

from home import serializers

# Create your views here.
@api_view(['GET'])
def home(request):
    api_urls = {
        'ACTIONS': 'ENDPOINT',
         'Users - All': '/users/',
        'User - Single': '/user/<str:pk>',
        'Articles - All': '/articles/',
        'Article - Single': '/articles/<str:pk>/',
        'Create Article': '/article-create/',
        'Update Article': '/article-update/<str:pk>',
        'Delete Article': '/article-delete/<str:pk>',
       
    }
    return Response(api_urls)


@api_view(['GET'])
def users(request):
    users = User.objects.all()
    serializer = UsersSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def articles(request):
    articles = Articles.objects.all()[::-1]
    serializer= ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def article(request, pk):
    article = Articles.objects.get(id=pk)
    serializer = ArticleSerializer(article, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def create_article(request):
    # article = Articles.objects.get(id=pk)
    serializer = ArticleSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def update_article(request, pk):
    article = Articles.objects.get(id=pk)
    serializer = ArticleSerializer(instance=article, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)



@api_view(['DELETE'])
def delete_article(request, pk):
    article = Articles.objects.get(id=pk)
    article.delete()
    return Response('Article delete successfully')