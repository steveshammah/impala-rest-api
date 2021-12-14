from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Articles(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    headline = models.CharField(max_length=250)
    content = models.TextField(max_length=None)
    image_1 = models.ImageField(upload_to='uploads/', blank=True)
    image_2 = models.ImageField(upload_to='uploads/', blank=True)
    type = models.CharField(max_length=100, null=True, default='article')
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
