from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class PlayersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = '__all__'


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


