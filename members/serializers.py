import re

from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
# from django.utils.translation import ugettext_lazy as _


class UsersSerializer(serializers.ModelSerializer):
    days_since_joined = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'days_since_joined']

    def get_days_since_joined(self, obj):
        return (now() - obj.date_joined).days
    

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