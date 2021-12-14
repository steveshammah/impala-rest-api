# from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='website-home'),
    path('users/', views.users, name='users-page'),
    path('articles/', views.articles, name='articles-page'),
    path('articles/<str:pk>/', views.article, name='article page'),
    path('article-create/', views.create_article, name='article create'),
    path('article-delete/<str:pk>', views.delete_article, name='article delete'),
    path('article-update/<str:pk>', views.update_article, name='article update'),
]
