# from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='website-home'),
    path('users/', views.get_all_users, name='users page'),
    path('users/<str:pk>/', views.get_user, name='user page'),
    path('authors/', views.get_all_authors, name='authors page'),
    path('authors/<str:pk>/', views.get_author, name='author page'),
    path('articles/', views.get_all_articles, name='articles page'),
    path('articles/<str:pk>/', views.get_article, name='article page'),
    path('article-create/', views.create_article, name='article create'),
    path('article-delete/<str:pk>', views.delete_article, name='article delete'),
    path('article-update/<str:pk>', views.update_article, name='article update'),
    path('products/', views.get_all_products, name='products page'),
    path('products/<str:pk>/', views.get_product, name='product page'),
]
