from django.shortcuts import render
from .models import Articles, Product, Author
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ArticleSerializer, UsersSerializer, ProductsSerializer, AuthorSerializer
# from django.http import JsonResponse
from django.contrib.auth.models import User
from home import serializers

# Create your views here.


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

    except Exception as error:
        return Response(f'Product with id {pk} not found')


# AUTHORS ENDPOINTS
@api_view(['GET'])
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
    except Exception as error:
        return Response(f'Author with id {pk} not found')


# ARTICLES ENDPOINTS
@api_view(['GET'])
def get_all_articles(request):
    # print('Getting all posts')
    articles = Articles.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_article(request, pk):
    try:
        article = Articles.objects.get(id=pk)
        serializer = ArticleSerializer(article, many=False)
        return Response(serializer.data)
    except Exception as error:
        # print('FILE NOT FOUND: ', error)
        return Response(f'Article with ID : {pk} Not Found')


@api_view(['POST'])
def create_article(request):
    # article = Articles.objects.get(id=pk)
    print('Article Create', request.data)
    serializer = ArticleSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
    else:
        print('Form is not valid')
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


# PRODUCTS ENDPOINTS
@api_view(['GET'])
def get_all_products(request):
    products = Product.objects.all()
    serializer = ProductsSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_product(request, pk):
    try:
        product = Product.objects.get(id=pk)
        serializer = ProductsSerializer(product, many=False)
        return Response(serializer.data)
    except Exception as error:
        return Response(f'Product with id {pk} not found')