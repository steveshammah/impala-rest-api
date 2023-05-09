from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        default="", upload_to='uploads/', null=True, blank=True)
    phone = models.CharField(max_length=100, default="")
    is_editor = models.BooleanField(default=0)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ('-user',)


class Tag(models.Model):
    tag = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.tag


class Article(models.Model):
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    headline = models.CharField(max_length=250)
    content_1 = models.TextField(max_length=None)
    image_1 = models.ImageField(upload_to='uploads/', null=True, blank=True)
    caption_1 = models.CharField(
        max_length=250, null=True, default='Impala Rugby')
    content_2 = models.TextField(max_length=None, null=True)
    image_2 = models.ImageField(upload_to='uploads/', null=True, blank=True)
    caption_2 = models.CharField(
        max_length=250, null=True, default='Impala Rugby')
    type = models.CharField(max_length=100, null=True, default='article')
    tags = models.CharField(max_length=150, null=True, default='Impala')
    created = models.DateTimeField(auto_now_add=True)
    posted = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title
