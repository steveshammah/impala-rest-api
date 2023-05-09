import re

from rest_framework import serializers
from django.contrib.auth.models import BaseUserManager, User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import password_validation
# from django.utils.translation import ugettext_lazy as _


from .models import *


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
        fields = ['id', 'player_name', 'profile_pic', 'team',
                  'social_link', 'date_of_birth', 'team', 'phone']


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
        fields = ["phone", "profile_pic",
                  "date_of_birth", "team", "social_link"]
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
            self.instance.date_of_birth = self.validated_data.get(
                "date_of_birth")
            self.instance.phone = self.validated_data.get("phone")
            self.instance.team = self.validated_data.get("team")
            self.instance.social_link = self.validated_data.get("social_link")
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
        model = Team
        fields = ["name", "logo", "description",
                  "home_ground", "location", "league"]
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
        model = Team
        fields = ["name", "logo", "description",
                  "home_ground", "location", "league"]
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