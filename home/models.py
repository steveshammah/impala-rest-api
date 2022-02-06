from unicodedata import name
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Author(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=15, null=True)
    profile_pic = models.ImageField(default="", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    is_staff = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-name',)


# class Player(models.Model):
#     username = models.ForeignKey(User, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=100, blank=True, null=True)
#     last_name = models.CharField(max_length=100, blank=True, null=True)
#     date_of_birth = models.DateField(blank=True)
#     phone = models.CharField(max_length=100)
#     email = models.EmailField(max_length=254)
#     date_joined = models.DateField(auto_now=False, auto_now_add=False)
#     date_created = models.DateTimeField(auto_now_add=True)
#     is_staff = models.BooleanField(default=False, null=True)


    # class Meta:
    #     ordering = ('-date_joined',)
    #
    # def __str__(self) -> str:
    #     return str(self.username)


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
        return str(self.title)


# class Fixtures(models.Model):
#     opponent = models.CharField(max_length=100)
#     match_date = models.DateField(None)
#     venue = models.CharField(max_length=100)
#     kickoff = models.CharField(max_length=20)


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


