from unicodedata import name
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Author(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    # name = models.CharField(max_length=100, null=True)
    profile_pic = models.ImageField(default="", upload_to='uploads/', null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ('-user',)


# class Player(models.Model):
#     user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
#     # first_name = models.CharField(max_length=100, blank=True, null=True)
#     # last_name = models.CharField(max_length=100, blank=True, null=True)
#     date_of_birth = models.DateField(blank=True, null=True)
#     # phone = models.CharField(max_length=100)
#     # email = models.EmailField(max_length=254)
#     team = models.CharField(max_length=150, null=True, blank=True)
#     social_link = models.CharField(max_length=150, null=True, blank=True)
#     # date_created = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         ordering = ('-user',)
#
#     def __str__(self) -> str:
#         return self.user.username


class Articles(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    headline = models.CharField(max_length=250)
    content_1 = models.TextField(max_length=None)
    content_2 = models.TextField(max_length=None, null=True)
    image_1 = models.ImageField(upload_to='uploads/', blank=True)
    caption_1 = models.CharField(max_length=250, null=True, default='Impala Rugby')
    image_2 = models.ImageField(upload_to='uploads/', blank=True)
    caption_2 = models.CharField(max_length=250, null=True, default='Impala Rugby')
    type = models.CharField(max_length=100, null=True, default='article')
    tags = models.CharField(max_length=150, null=True, default='Impala')
    created = models.DateTimeField(auto_now_add=True)
    posted = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    # PRODUCT_TYPE = ('Jersey', 'Hoodies', 'T-shirt', 'sweat-gear', 'a')
    name = models.CharField(max_length=150, blank=True, null=True)
    image = models.ImageField(null=True, blank=True, default='/placeholder.png')
    price = models.IntegerField()
    description = models.TextField(max_length=500)
    color = models.CharField(max_length=100, blank=True, null=True)
    count_in_stock = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-name',)


# class Team(models.Model):
#     name = models.CharField(max_length=150, blank=True, null=True)
#     logo = models.ImageField(null=True, blank=True, default='/placeholder.png')
#     description = models.TextField(max_length=500)
#     home_ground = models.CharField(max_length=100)
#     location = models.CharField(max_length=100)
#     league = models.CharField(max_length=100, blank=True, null=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         ordering = ('-name',)


# class Fixtures(models.Model):
#     opponent = models.CharField(max_length=100)
#     match_date = models.DateField(None)
#     venue = models.CharField(max_length=100)
#     kickoff = models.CharField(max_length=20)


# class Partner(models.Model):
#     name = models.CharField(max_length=150, blank=True, null=True)
#     logo = models.ImageField(null=True, blank=True, default='/placeholder.png')
#     about = models.TextField(max_length=500)
#     tag = models.CharField(max_length=200, null=True, blank=True)
#     url = models.CharField(max_length=100, null=True, blank=True)
#     website = models.CharField(max_length=200, blank=True, null=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         ordering = ('-name',)


