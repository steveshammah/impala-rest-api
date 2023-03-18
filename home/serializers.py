import re

from rest_framework import serializers
from django.contrib.auth.models import BaseUserManager, User
from datetime import date
from django.utils.timezone import now
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, password_validation
# from django.utils.translation import ugettext_lazy as _


from .models import *


class UsersSerializer(serializers.ModelSerializer):
    days_since_joined = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'days_since_joined']

    def get_days_since_joined(self, obj):
        return (now() - obj.date_joined).days


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
        fields = ["username", "phone", "first_name", "last_name", "email", "profile_pic", "is_editor", "password"]
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
                    self.instance.profile_pic = self.validated_data.get("profile_pic")
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


class PlayerSerializer(serializers.ModelSerializer):
    player_name = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        source='user'
    )
    team = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Team.objects.all(),
    )

    class Meta:
        model = Player
        fields = ['id', 'player_name', 'profile_pic', 'team', 'social_link', 'date_of_birth', 'team', 'phone']


class ListPlayerSerializer(serializers.ModelSerializer):

    player_name = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        source='user'
    )
    team = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Team.objects.all(),
    )

    class Meta:
        model = Player
        fields = ['player_name', 'team', 'social_link']


class CreatePlayerSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    date_of_birth = serializers.DateField()
    profile_pic = serializers.ImageField(required=False)
    phone = serializers.CharField(max_length=22, required=True)
    team = serializers.CharField(max_length=22, required=True)
    social_link = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        trim_whitespace=False,
        max_length=255,
        write_only=True,
        validators=[validate_password],
    )

    class Meta:
        model = Player
        fields = ["username", "phone", "first_name", "last_name", "email", "profile_pic",
                  "date_of_birth", "team", "social_link", "password"]
        validators: list = []

    def validate_username(self, value):
        user = User.objects.filter(username=value)
        if user:
            raise serializers.ValidationError("Username already taken")
        return value

    def validate_first_name(self, value):
        # evaluate whether all characters are letters
        return value

    def validate_last_name(self, value):
        # evaluate whether all characters are letters
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

    def validate_team(self, value):
        team = Team.objects.get(name=value)
        value = team
        return value

    def validate_social_link(self, value):
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

            player_profile = Player.objects.create(
                user=user,
                date_of_birth=validated_data['date_of_birth'],
                phone=validated_data['phone'],
                # profile_pic=validated_data['profile_pic'],
                team=validated_data['team'],
                social_link=validated_data['social_link'],
            )
            player_profile.save()

            validated_data["user"] = user
            validated_data["player"] = player_profile

            validated_data.pop("username")
            validated_data.pop("first_name")
            validated_data.pop("last_name")
            validated_data.pop("email")
            validated_data.pop("password")

        except Exception:
            raise serializers.ValidationError("Player creation failed.")

        return validated_data


class UpdatePlayerSerializer(serializers.Serializer):
    date_of_birth = serializers.DateField()
    profile_pic = serializers.ImageField(required=False)
    phone = serializers.CharField(max_length=22, required=True)
    team = serializers.CharField(max_length=22, required=True)
    social_link = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = Player
        fields = ["phone", "profile_pic", "date_of_birth", "team", "social_link"]
        validators: list = []

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

    def validate_team(self, value):
        try:
            team = Team.objects.get(name=value)
            value = team
        except Exception:
            raise serializers.ValidationError("Please enter a valid team")
        return value

    def validate_social_link(self, value):
        return value

    def save(self, *args, **kwargs):
        if self.partial:
            if self.validated_data:
                if self.validated_data.get("phone"):
                    self.instance.phone = self.validated_data.get("phone")
                if self.validated_data.get("profile_pic"):
                    self.instance.profile_pic = self.validated_data.get(
                        "profile_pic")
                if self.validated_data.get("date_of_birth"):
                    self.instance.date_of_birth = self.validated_data.get(
                        "date_of_birth")
                if self.validated_data.get("team"):
                    self.instance.team = self.validated_data.get(
                        "team")
                if self.validated_data.get("social_link"):
                    self.instance.social_link = self.validated_data.get(
                        "social_link")
                self.instance.save()
            else:
                return "No data to update"
        else:
            self.instance.profile_pic = self.validated_data.get("profile_pic")
            self.instance.date_of_birth = self.validated_data.get("date_of_birth")
            self.instance.phone = self.validated_data.get("phone")
            self.instance.team = self.validated_data.get("team")
            self.instance.social_link = self.validated_data.get("social_link")
            self.instance.save()


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Article
        # fields = '__all__'
        exclude = ['created']

    def get_author(self, obj):
        return obj.author.user.username


class ListArticleSerializer(serializers.ModelSerializer):
    article_author = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['article_author', 'title', 'content_1', 'image_1']

    def get_article_author(self, obj):
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
            raise serializers.ValidationError("The title entered already exists.")
        return value

    def validate_headline(self, value):
        article = Article.objects.get(headline=value)
        if article:
            raise serializers.ValidationError("The headline entered already exists.")
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


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class ListTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'location', 'league']


class CreateTeamSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    logo = serializers.ImageField()
    description = serializers.CharField()
    home_ground = serializers.CharField()
    location = serializers.CharField()
    league = serializers.CharField()

    class Meta:
        model = Author
        fields = ["name", "logo", "description", "home_ground", "location", "league"]
        validators: list = []

    def validate_name(self, value):
        return value

    def validate_logo(self, value):
        return value

    def validate_description(self, value):
        return value

    def validate_home_ground(self, value):
        return value

    def validate_location(self, value):
        return value

    def validate_league(self, value):
        return value

    def create(self, validated_data):
        try:
            team = Team.objects.create(
                name=validated_data['name'],
                logo=validated_data['logo'],
                description=validated_data['description'],
                home_ground=validated_data['home_ground'],
                location=validated_data['location'],
                league=validated_data['league'],
            )
            team.save()

            validated_data["team"] = team

        except Exception:
            raise serializers.ValidationError("Team creation failed.")

        return validated_data


class UpdateTeamSerializer(serializers.Serializer):
    name = serializers.CharField()
    logo = serializers.ImageField(required=False)
    description = serializers.CharField()
    home_ground = serializers.CharField()
    location = serializers.CharField()
    league = serializers.CharField()

    class Meta:
        model = Author
        fields = ["name", "logo", "description", "home_ground", "location", "league"]
        validators: list = []

    def validate_name(self, value):
        return value

    def validate_logo(self, value):
        return value

    def validate_description(self, value):
        return value

    def validate_home_ground(self, value):
        return value

    def validate_location(self, value):
        return value

    def validate_league(self, value):
        return value

    def save(self, *args, **kwargs):
        if self.partial:
            if self.validated_data:
                if self.validated_data.get("name"):
                    self.instance.name = self.validated_data.get("name")
                if self.validated_data.get("logo"):
                    self.instance.logo = self.validated_data.get(
                        "logo")
                if self.validated_data.get("description"):
                    self.instance.description = self.validated_data.get(
                        "description")
                if self.validated_data.get("home_ground"):
                    self.instance.home_ground = self.validated_data.get(
                        "home_ground")
                if self.validated_data.get("location"):
                    self.instance.location = self.validated_data.get(
                        "location")
                if self.validated_data.get("league"):
                    self.instance.league = self.validated_data.get(
                        "league")
                self.instance.save()
            else:
                return "No data to update"
        else:
            self.instance.name = self.validated_data.get("name")
            self.instance.logo = self.validated_data.get("logo")
            self.instance.description = self.validated_data.get("description")
            self.instance.home_ground = self.validated_data.get("home_ground")
            self.instance.location = self.validated_data.get("location")
            self.instance.league = self.validated_data.get("league")
            self.instance.save()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ListProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'image', 'price', 'description']


class CreateProductSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField()
    image = serializers.ImageField(required=False)
    description = serializers.CharField()
    price = serializers.CharField()
    color = serializers.CharField()
    count_in_stock = serializers.CharField()

    class Meta:
        model = Product
        fields = ['product_name', 'image', 'price', 'description', 'color', 'count_in_stock']
        validators: list = []

    def validate_product_name(self, value):
        if value not in ["Jersey", "Hoodie", "Tshirt", "Sweater", "Watterbottle"]:
            raise serializers.ValidationError("The selection has to be Jersey, Hoodie, Tshirt, Sweater or Watterbottle")
        return value

    def validate_image(self, value):
        return value

    def validate_description(self, value):
        return value

    def validate_price(self, value):
        return value

    def validate_color(self, value):
        return value

    def validate_count_in_stock(self, value):
        return value

    def create(self, validated_data):
        try:
            product = Product.objects.create(
                product_name=validated_data['product_name'],
                # image=validated_data['image'],
                description=validated_data['description'],
                price=validated_data['price'],
                color=validated_data['color'],
                count_in_stock=validated_data['count_in_stock'],
            )
            product.save()

            validated_data["product"] = product

        except Exception:
            raise serializers.ValidationError("Product creation failed.")

        return validated_data


class UpdateProductSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    image = serializers.ImageField(required=False)
    description = serializers.CharField()
    price = serializers.CharField()
    color = serializers.CharField()
    count_in_stock = serializers.CharField()

    class Meta:
        model = Product
        fields = ['product_name', 'image', 'price', 'description', 'color', 'count_in_stock']
        validators: list = []

    def validate_product_name(self, value):
        if value not in ["Jersey", "Hoodie", "Tshirt", "Sweater", "Watterbottle"]:
            raise serializers.ValidationError("The selection has to be Jersey, Hoodie, Tshirt, Sweater or Watterbottle")
        return value

    def validate_image(self, value):
        return value

    def validate_description(self, value):
        return value

    def validate_price(self, value):
        return value

    def validate_color(self, value):
        return value

    def validate_count_in_stock(self, value):
        return value

    def save(self, *args, **kwargs):
        if self.partial:
            if self.validated_data:
                if self.validated_data.get("product_name"):
                    self.instance.product_name = self.validated_data.get("product_name")
                if self.validated_data.get("image"):
                    self.instance.image = self.validated_data.get(
                        "image")
                if self.validated_data.get("description"):
                    self.instance.description = self.validated_data.get(
                        "description")
                if self.validated_data.get("price"):
                    self.instance.price = self.validated_data.get(
                        "price")
                if self.validated_data.get("color"):
                    self.instance.color = self.validated_data.get(
                        "color")
                if self.validated_data.get("count_in_stock"):
                    self.instance.count_in_stock = self.validated_data.get(
                        "count_in_stock")
                self.instance.save()
            else:
                return "No data to update"
        else:
            self.instance.product_name = self.validated_data.get("product_name")
            self.instance.image = self.validated_data.get("image")
            self.instance.description = self.validated_data.get("description")
            self.instance.price = self.validated_data.get("price")
            self.instance.color = self.validated_data.get("color")
            self.instance.count_in_stock = self.validated_data.get("count_in_stock")
            self.instance.save()


class FixtureSerializer(serializers.ModelSerializer):
    home_team = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Team.objects.all(),
    )
    away_team = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Team.objects.all(),
    )

    class Meta:
        model = Fixture
        fields = '__all__'


class ListFixtureSerializer(serializers.ModelSerializer):
    home_team = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Team.objects.all(),
    )
    away_team = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Team.objects.all(),
    )

    class Meta:
        model = Fixture
        fields = ['id', 'home_team', 'away_team', 'match_date', 'venue']


class CreateFixtureSerializer(serializers.ModelSerializer):
    home_team = serializers.CharField()
    away_team = serializers.CharField()
    match_date = serializers.DateField()
    venue = serializers.CharField()
    kickoff = serializers.CharField()

    class Meta:
        model = Fixture
        fields = ['home_team', 'away_team', 'match_date', 'venue', 'kickoff']
        validators: list = []

    def validate_home_team(self, value):
        try:
            team = Team.objects.get(name=value)
            value = team
        except Exception:
            raise serializers.ValidationError("Please enter a valid team")
        return value

    def validate_away_team(self, value):
        try:
            team = Team.objects.get(name=value)
            value = team
        except Exception:
            raise serializers.ValidationError("Please enter a valid team")
        return value

    def validate_match_date(self, value):
        return value

    def validate_venue(self, value):
        return value

    def validate_kickoff(self, value):
        return value

    def validate(self, attrs):
        instance = Fixture(**attrs)
        instance.clean()
        return attrs

    def create(self, validated_data):
        try:
            fixture = Fixture.objects.create(
                home_team=validated_data['home_team'],
                away_team=validated_data['away_team'],
                match_date=validated_data['match_date'],
                venue=validated_data['venue'],
                kickoff=validated_data['kickoff'],
            )
            fixture.save()

            validated_data["fixture"] = fixture

        except Exception:
            raise serializers.ValidationError("Fixture creation failed.")

        return validated_data


class UpdateFixtureSerializer(serializers.Serializer):
    home_team = serializers.CharField()
    away_team = serializers.CharField()
    match_date = serializers.DateField()
    venue = serializers.CharField()
    kickoff = serializers.CharField()

    class Meta:
        model = Fixture
        fields = ['home_team', 'away_team', 'match_date', 'venue', 'kickoff']
        validators: list = []

    def validate_home_team(self, value):
        try:
            team = Team.objects.get(name=value)
            value = team
        except Exception:
            raise serializers.ValidationError("Please enter a valid team")
        return value

    def validate_away_team(self, value):
        try:
            team = Team.objects.get(name=value)
            value = team
        except Exception:
            raise serializers.ValidationError("Please enter a valid team")
        return value

    def validate_match_date(self, value):
        return value

    def validate_venue(self, value):
        return value

    def validate_kickoff(self, value):
        return value

    def validate(self, attrs):
        instance = Fixture(**attrs)
        instance.clean()
        return attrs

    def save(self, *args, **kwargs):
        if self.partial:
            if self.validated_data:
                if self.validated_data.get("home_team"):
                    self.instance.home_team = self.validated_data.get("home_team")
                if self.validated_data.get("away_team"):
                    self.instance.away_team = self.validated_data.get(
                        "away_team")
                if self.validated_data.get("match_date"):
                    self.instance.match_date = self.validated_data.get(
                        "match_date")
                if self.validated_data.get("venue"):
                    self.instance.venue = self.validated_data.get(
                        "venue")
                if self.validated_data.get("kickoff"):
                    self.instance.kickoff = self.validated_data.get(
                        "kickoff")
                self.instance.save()
            else:
                return "No data to update"
        else:
            self.instance.home_team = self.validated_data.get("home_team")
            self.instance.away_team = self.validated_data.get("away_team")
            self.instance.match_date = self.validated_data.get("match_date")
            self.instance.venue = self.validated_data.get("venue")
            self.instance.kickoff = self.validated_data.get("kickoff")
            self.instance.save()


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'


class ListPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['id', 'name', 'website']


class CreatePartnerSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    logo = serializers.ImageField(required=False)
    about = serializers.CharField()
    tag = serializers.CharField()
    url = serializers.CharField()
    website = serializers.CharField()

    class Meta:
        model = Partner
        fields = ['name', 'logo', 'about', 'tag', 'url', 'website']
        validators: list = []

    def validate_name(self, value):
        return value

    def validate_logo(self, value):
        return value

    def validate_about(self, value):
        return value

    def validate_tag(self, value):
        return value

    def validate_url(self, value):
        return value

    def validate_website(self, value):
        return value

    def create(self, validated_data):
        try:
            partner = Partner.objects.create(
                name=validated_data['name'],
                # logo=validated_data['logo'],
                about=validated_data['about'],
                tag=validated_data['tag'],
                url=validated_data['url'],
                website=validated_data['website']
            )
            partner.save()

            validated_data["partner"] = partner

        except Exception:
            raise serializers.ValidationError("Partner creation failed.")

        return validated_data


class UpdatePartnerSerializer(serializers.Serializer):
    name = serializers.CharField()
    logo = serializers.ImageField(required=False)
    about = serializers.CharField()
    tag = serializers.CharField()
    url = serializers.CharField()
    website = serializers.CharField()

    class Meta:
        model = Partner
        fields = ['name', 'logo', 'about', 'tag', 'url', 'website']
        validators: list = []

    def validate_name(self, value):
        return value

    def validate_logo(self, value):
        return value

    def validate_about(self, value):
        return value

    def validate_tag(self, value):
        return value

    def validate_url(self, value):
        return value

    def validate_website(self, value):
        return value

    def save(self, *args, **kwargs):
        if self.partial:
            if self.validated_data:
                if self.validated_data.get("name"):
                    self.instance.name = self.validated_data.get("name")
                if self.validated_data.get("logo"):
                    self.instance.logo = self.validated_data.get(
                        "logo")
                if self.validated_data.get("about"):
                    self.instance.about = self.validated_data.get(
                        "about")
                if self.validated_data.get("tag"):
                    self.instance.tag = self.validated_data.get(
                        "tag")
                if self.validated_data.get("url"):
                    self.instance.url = self.validated_data.get(
                        "url")
                if self.validated_data.get("website"):
                    self.instance.website = self.validated_data.get(
                        "website")
                self.instance.save()
            else:
                return "No data to update"
        else:
            self.instance.name = self.validated_data.get("name")
            self.instance.logo = self.validated_data.get("logo")
            self.instance.about = self.validated_data.get("about")
            self.instance.tag = self.validated_data.get("tag")
            self.instance.url = self.validated_data.get("url")
            self.instance.website = self.validated_data.get("website")
            self.instance.save()


class UserSignInSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        trim_whitespace=False,
        max_length=255,
        write_only=True,
        validators=[validate_password],
    )

    # Validate username
    def validate_username(self, value):
        user = User.objects.filter(username=value)
        if not user:
            raise serializers.ValidationError("Invalid! Try again.")
        return value

    # Validate password
    def validate_password(self, value):
        validate_password(value)
        return value

    # Validate credentials provided
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                raise serializers.ValidationError('Unable to log in with provided credentials.', code='authorization')
        else:
            raise serializers.ValidationError('Must include username and password.', code='authorization')

        data['user'] = user
        return data


class SmsModelSerializer(serializers.ModelSerializer):
    code = serializers.CharField(
        max_length=8, required=True, help_text='Enter code')

    class Meta:
        model = SmsModel
        fields = ["code"]
        validators: list = []

    def validate_code(self, value):
        code_regex = "^[0-9]{6}$"
        regexed_code = re.search(code_regex, value)

        if regexed_code:
            value = re.sub(r'[^0-9]', '', value)
        else:
            raise serializers.ValidationError(
                "Code must be 6 digits.")
        return value


class FixtureResultSerializer(serializers.ModelSerializer):
    home_team_result = serializers.IntegerField()
    away_team_result = serializers.IntegerField()
    fixture = serializers.SerializerMethodField()
    MOTM = serializers.SerializerMethodField()

    class Meta:
        model = FixtureResult
        fields = '__all__'

    def get_fixture(self, obj):
        return f'{obj.fixture.id}. {obj.fixture.home_team} VS {obj.fixture.away_team}'

    def get_MOTM(self, obj):
        return obj.MOTM.user.username


class ListFixtureResultSerializer(serializers.ModelSerializer):
    home_team_result = serializers.IntegerField()
    away_team_result = serializers.IntegerField()
    fixture = serializers.SerializerMethodField()
    MOTM = serializers.SerializerMethodField()

    class Meta:
        model = FixtureResult
        fields = ['fixture', 'home_team_result', 'away_team_result', 'MOTM']

    def get_fixture(self, obj):
        return f'{obj.fixture.id}. {obj.fixture.home_team} VS {obj.fixture.away_team}'

    def get_MOTM(self, obj):
        return obj.MOTM.user.username


class CreateFixtureResultSerializer(serializers.ModelSerializer):
    fixture = serializers.CharField()
    home_team_result = serializers.IntegerField()
    away_team_result = serializers.IntegerField()
    MOTM = serializers.CharField()

    class Meta:
        model = FixtureResult
        fields = ['fixture', 'home_team_result', 'away_team_result', 'MOTM']
        validators: list = []

    def validate_fixture(self, value):
        fixture = Fixture.objects.get(id=value)
        fixture_results = fixture.associated_fixture.all().count()

        if fixture_results:
            raise serializers.ValidationError("A fixture cannot have more than one result.")
        value = fixture
        return value

    def validate_home_team_result(self, value):
        return value

    def validate_away_team_result(self, value):
        return value

    def validate_MOTM(self, value):
        player = Player.objects.get(id=value)
        value = player
        return value

    def create(self, validated_data):
        try:
            fixture_result = FixtureResult.objects.create(
                fixture=validated_data['fixture'],
                home_team_result=validated_data['home_team_result'],
                away_team_result=validated_data['away_team_result'],
                MOTM=validated_data['MOTM']
            )
            fixture_result.save()

            validated_data["fixture_result"] = fixture_result

        except Exception:
            raise serializers.ValidationError("Fixture-result creation failed.")

        return validated_data


class UpdateFixtureResultSerializer(serializers.Serializer):
    fixture = serializers.CharField()
    home_team_result = serializers.IntegerField()
    away_team_result = serializers.IntegerField()
    MOTM = serializers.CharField()

    class Meta:
        model = Partner
        fields = ['fixture', 'home_team_result', 'away_team_result', 'MOTM']
        validators: list = []

    def validate_fixture(self, value):
        fixture = Fixture.objects.get(id=value)

        if not self.instance.fixture == fixture:
            raise serializers.ValidationError("The fixture must be the same.")
        value = fixture
        return value

    def validate_home_team_result(self, value):
        return value

    def validate_away_team_result(self, value):
        return value

    def validate_MOTM(self, value):
        player = Player.objects.get(id=value)
        value = player
        return value

    def save(self, *args, **kwargs):
        if self.partial:
            if self.validated_data:
                if self.validated_data.get("fixture"):
                    self.instance.fixture = self.validated_data.get("fixture")
                if self.validated_data.get("home_team_result"):
                    self.instance.home_team_result = self.validated_data.get(
                        "home_team_result")
                if self.validated_data.get("away_team_result"):
                    self.instance.away_team_result = self.validated_data.get(
                        "away_team_result")
                if self.validated_data.get("MOTM"):
                    self.instance.MOTM = self.validated_data.get(
                        "MOTM")
                self.instance.save()
            else:
                return "No data to update"
        else:
            self.instance.fixture = self.validated_data.get("fixture")
            self.instance.home_team_result = self.validated_data.get("home_team_result")
            self.instance.away_team_result = self.validated_data.get("away_team_result")
            self.instance.MOTM = self.validated_data.get("MOTM")
            self.instance.save()
