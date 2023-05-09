import re

from rest_framework import serializers
# from django.utils.translation import ugettext_lazy as _


from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'image', 'price',
                  'description', 'color', 'count_in_stock']
        validators: list = []

    def validate_product_name(self, value):
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
                    self.instance.product_name = self.validated_data.get(
                        "product_name")
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
            self.instance.product_name = self.validated_data.get(
                "product_name")
            self.instance.image = self.validated_data.get("image")
            self.instance.description = self.validated_data.get("description")
            self.instance.price = self.validated_data.get("price")
            self.instance.color = self.validated_data.get("color")
            self.instance.count_in_stock = self.validated_data.get(
                "count_in_stock")
            self.instance.save()


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
        fields = ['product_name', 'image', 'price',
                  'description', 'color', 'count_in_stock']
        validators: list = []

    def validate_product_name(self, value):
        if value not in ["Jersey", "Hoodie", "Tshirt", "Sweater", "Watterbottle"]:
            raise serializers.ValidationError(
                "The selection has to be Jersey, Hoodie, Tshirt, Sweater or Watterbottle")
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
        fields = ['product_name', 'image', 'price',
                  'description', 'color', 'count_in_stock']
        validators: list = []

    def validate_product_name(self, value):
        if value not in ["Jersey", "Hoodie", "Tshirt", "Sweater", "Watterbottle"]:
            raise serializers.ValidationError(
                "The selection has to be Jersey, Hoodie, Tshirt, Sweater or Watterbottle")
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
                    self.instance.product_name = self.validated_data.get(
                        "product_name")
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
            self.instance.product_name = self.validated_data.get(
                "product_name")
            self.instance.image = self.validated_data.get("image")
            self.instance.description = self.validated_data.get("description")
            self.instance.price = self.validated_data.get("price")
            self.instance.color = self.validated_data.get("color")
            self.instance.count_in_stock = self.validated_data.get(
                "count_in_stock")
            self.instance.save()