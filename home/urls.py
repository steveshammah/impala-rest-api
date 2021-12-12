# from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='website-home'),
    # path('fixtures/',views.fixtures,name='fixtures-page'),
    # path('videos/',views.videos,name='videos-page'),
    path('articles/',views.articles,name='articles-page'),
    path('articles/<str:pk>/',views.article,name='article page'),
    path('article-create/',views.create_article,name='article creation'),
    path('article-update/<str:pk>',views.update_article,name='article update'),
    path('users/',views.users,name='users-page'),
    # path('contact-us/',views.contact_us,name='contact-page'),
    # path('visit-impala/',views.visit_impala,name='visit-impala'),
]