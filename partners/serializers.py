import re
from rest_framework import serializers
# from django.utils.translation import ugettext_lazy as _

from .models import *


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