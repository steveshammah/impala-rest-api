import re

from rest_framework import serializers
from django.contrib.auth.models import BaseUserManager, User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import password_validation
# from django.utils.translation import ugettext_lazy as _


from .models import *


class AuthorSerializer(serializers.ModelSerializer):
    author_name = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        source='user',
    )

    class Meta:
        model = Author
        fields = ['id', 'author_name', 'profile_pic', 'is_editor', 'phone']


class ListAuthorSerializer(serializers.ModelSerializer):
    author_name = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        source='user',
    )

    class Meta:
        model = Author
        fields = ['author_name', 'is_editor', 'phone']


class CreateAuthorSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    profile_pic = serializers.ImageField(required=False)
    phone = serializers.CharField(max_length=22, required=True)
    is_editor = serializers.IntegerField()
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        trim_whitespace=False,
        max_length=255,
        write_only=True,
        validators=[validate_password],
    )

    class Meta:
        model = Author
        fields = ["username", "phone", "first_name", "last_name",
                  "email", "profile_pic", "is_editor", "password"]
        validators: list = []

    def validate_username(self, value):
        user = User.objects.filter(username=value)
        if user:
            raise serializers.ValidationError("Username already taken")
        return value

    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user:
            raise serializers.ValidationError("Email is already taken")
        return BaseUserManager.normalize_email(value)

    def validate_phone(self, value):
        telephone_regex = "^\+\({1}\d{1,4}\){1}([\s.-])\d{3,4}[\s.-]?\d{2,4}[\s.-]?\d{2,4}$"
        regexed_telephone = re.search(telephone_regex, value)

        if regexed_telephone:
            value = re.sub(r'[^0-9]', '', value)
            value = "+" + value
        else:
            raise serializers.ValidationError(
                "Wrong format. Please use the format: +(COUNTRYCODE)-NATIONALNUMBER e.g. +(12)-34567890")
        return value

    def validate_profile_pic(self, value):
        return value

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        try:
            user = User.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
            )
            user.set_password(validated_data['password'])
            user.is_active = True
            user.save()

            author_profile = Author.objects.create(
                user=user,
                # profile_pic=validated_data['profile_pic'],
                phone=validated_data['phone'],
                is_editor=validated_data['is_editor'],
            )
            author_profile.save()

            validated_data["author"] = author_profile

            validated_data.pop("username")
            validated_data.pop("first_name")
            validated_data.pop("last_name")
            validated_data.pop("email")
            validated_data.pop("password")

        except Exception:
            raise serializers.ValidationError("Author creation failed.")

        return validated_data


class UpdateAuthorSerializer(serializers.Serializer):
    profile_pic = serializers.ImageField(required=False)
    is_editor = serializers.IntegerField()
    phone = serializers.CharField(max_length=22)

    class Meta:
        model = Author
        fields = ["profile_pic", "phone", "is_editor"]
        validators: list = []

    def validate_profile_pic(self, value):
        return value

    def validate_phone(self, value):
        telephone_regex = "^\+\({1}\d{1,4}\){1}([\s.-])\d{3,4}[\s.-]?\d{2,4}[\s.-]?\d{2,4}$"
        regexed_telephone = re.search(telephone_regex, value)

        if regexed_telephone:
            value = re.sub(r'[^0-9]', '', value)
            value = "+" + value
        else:
            raise serializers.ValidationError(
                "Wrong format. Please use the format: +(COUNTRYCODE)-NATIONALNUMBER e.g. +(12)-34567890")
        return value

    def validate_is_editor(self, value):
        if int(value) not in [0, 1]:
            raise serializers.ValidationError(
                "Value can only be 0 or 1.")
        return value

    def save(self, *args, **kwargs):
        if self.partial:
            if self.validated_data:
                if self.validated_data.get("profile_pic"):
                    self.instance.profile_pic = self.validated_data.get(
                        "profile_pic")
                if self.validated_data.get("is_editor"):
                    self.instance.is_editor = self.validated_data.get(
                        "is_editor")
                if self.validated_data.get("phone"):
                    self.instance.phone = self.validated_data.get(
                        "phone")
                self.instance.save()
            else:
                return "No data to update"
        else:
            self.instance.profile_pic = self.validated_data.get("profile_pic")
            self.instance.is_editor = self.validated_data.get("is_editor")
            self.instance.phone = self.validated_data.get("phone")
            self.instance.save()


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Article
        # fields = '__all__'
        exclude = ['created']

    def get_author(self, obj) -> str:
        return obj.author.user.username


class ListArticleSerializer(serializers.ModelSerializer):
    article_author = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['article_author', 'title', 'content_1', 'image_1']

    def get_article_author(self, obj) -> str:
        return obj.author.user.username


class CreateArticleSerializer(serializers.ModelSerializer):
    author = serializers.CharField()
    title = serializers.CharField()
    headline = serializers.CharField()
    content_1 = serializers.CharField()
    content_2 = serializers.CharField()
    image_1 = serializers.ImageField()
    caption_1 = serializers.CharField()
    image_2 = serializers.ImageField()
    caption_2 = serializers.CharField()
    type = serializers.CharField()
    tags = serializers.CharField()

    class Meta:
        model = Article
        fields = ["author", "title", "headline", "content_1", "content_2",
                  "image_1", "image_2", "caption_1", "caption_2", "type", "tags"]
        validators: list = []

    def validate_author(self, value):
        try:
            author = Author.objects.get(id=value)
            value = author
        except Exception:
            raise serializers.ValidationError("Please enter a valid author id")
        return value

    def validate_title(self, value):
        article = Article.objects.get(title=value)
        if article:
            raise serializers.ValidationError(
                "The title entered already exists.")
        return value

    def validate_headline(self, value):
        article = Article.objects.get(headline=value)
        if article:
            raise serializers.ValidationError(
                "The headline entered already exists.")
        return value

    def validate_content_1(self, value):
        return value

    def validate_content_2(self, value):
        return value

    def validate_caption_1(self, value):
        return value

    def validate_caption_2(self, value):
        return value

    def validate_image_1(self, value):
        return value

    def validate_image_2(self, value):
        return value

    def validate_type(self, value):
        return value

    def validate_tags(self, value):
        return value

    def create(self, validated_data):
        try:
            article = Article.objects.create(
                author=validated_data['author'],
                title=validated_data['title'],
                headline=validated_data['headline'],
                content_1=validated_data['content_1'],
                content_2=validated_data['content_2'],
                image_1=validated_data['image_1'],
                image_2=validated_data['image_2'],
                caption_1=validated_data['caption_1'],
                caption_2=validated_data['caption_2'],
                type=validated_data['type'],
                tags=validated_data['tags'],
            )
            article.save()

            validated_data["article"] = article

        except Exception:
            raise serializers.ValidationError("Article creation failed.")

        return validated_data


class UpdateArticleSerializer(serializers.Serializer):
    author = serializers.CharField()
    title = serializers.CharField()
    headline = serializers.CharField()
    content_1 = serializers.CharField()
    content_2 = serializers.CharField()
    image_1 = serializers.ImageField()
    caption_1 = serializers.CharField()
    image_2 = serializers.ImageField()
    caption_2 = serializers.CharField()
    type = serializers.CharField()
    tags = serializers.CharField()

    class Meta:
        model = Article
        fields = ["author", "title", "headline", "content_1", "content_2",
                  "image_1", "image_2", "caption_1", "caption_2", "type", "tags"]
        validators: list = []

    def validate_author(self, value):
        try:
            author = Author.objects.get(id=value)
            value = author
        except Exception:
            raise serializers.ValidationError("Please enter a valid author id")
        return value

    def validate_title(self, value):
        return value

    def validate_headline(self, value):
        return value

    def validate_content_1(self, value):
        return value

    def validate_content_2(self, value):
        return value

    def validate_caption_1(self, value):
        return value

    def validate_caption_2(self, value):
        return value

    def validate_image_1(self, value):
        return value

    def validate_image_2(self, value):
        return value

    def validate_type(self, value):
        return value

    def validate_tags(self, value):
        return value

    def save(self, *args, **kwargs):
        if self.partial:
            if self.validated_data:
                if self.validated_data.get("author"):
                    self.instance.author = self.validated_data.get("author")
                if self.validated_data.get("title"):
                    self.instance.title = self.validated_data.get(
                        "title")
                if self.validated_data.get("headline"):
                    self.instance.headline = self.validated_data.get(
                        "headline")
                if self.validated_data.get("content_1"):
                    self.instance.content_1 = self.validated_data.get(
                        "content_1")
                if self.validated_data.get("content_2"):
                    self.instance.content_2 = self.validated_data.get(
                        "content_2")
                if self.validated_data.get("image_1"):
                    self.instance.image_1 = self.validated_data.get(
                        "image_1")
                if self.validated_data.get("image_2"):
                    self.instance.image_2 = self.validated_data.get(
                        "image_2")
                if self.validated_data.get("caption_1"):
                    self.instance.caption_1 = self.validated_data.get(
                        "caption_1")
                if self.validated_data.get("caption_2"):
                    self.instance.caption_2 = self.validated_data.get(
                        "caption_2")
                if self.validated_data.get("type"):
                    self.instance.type = self.validated_data.get(
                        "type")
                if self.validated_data.get("tags"):
                    self.instance.tags = self.validated_data.get(
                        "tags")
                self.instance.save()
            else:
                return "No data to update"
        else:
            self.instance.author = self.validated_data.get("author")
            self.instance.title = self.validated_data.get("title")
            self.instance.headline = self.validated_data.get("headline")
            self.instance.content_1 = self.validated_data.get("content_1")
            self.instance.content_2 = self.validated_data.get("content_2")
            self.instance.image_1 = self.validated_data.get("image_1")
            self.instance.image_2 = self.validated_data.get("image_2")
            self.instance.caption_1 = self.validated_data.get("caption_1")
            self.instance.caption_2 = self.validated_data.get("caption_2")
            self.instance.type = self.validated_data.get("type")
            self.instance.tags = self.validated_data.get("tags")
            self.instance.save()
