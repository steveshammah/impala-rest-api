from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    def __str__(self):
        return self.name

class Articles(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    headline = models.CharField(max_length=250)
    content_1 = models.TextField(max_length=None)
    content_2 = models.TextField(max_length=None, null=True)
    image_1 = models.ImageField(upload_to='uploads/', blank=True)
    caption_1 = models.CharField(max_length=250, null=True, default='Impala Rugby')
    image_2 = models.ImageField(upload_to='uploads/', blank=True)
    caption_2 = models.CharField(max_length=250, null=True, default='Impala Rugby')
    type = models.CharField(max_length=100, null=True, default='article')
    tags = models.TextField(max_length=150, null=True, default='Impala')
    created = models.DateTimeField(auto_now_add=True)
    posted = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self) -> str:
        return str(self.title)



class Player(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True)
    phone= models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    date_joined = models.DateField(auto_now=False, auto_now_add=False)
    date_created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ('-date_joined',)

    def __str__(self) -> str:
        return str(self.username)


# class Fixtures(models.Model):
#     opponent = models.CharField(max_length=100)
#     match_date = models.DateField(None)
#     venue = models.CharField(max_length=100)
#     kickoff = models.CharField(max_length=20)
