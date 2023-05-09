from django.db import models


class Partner(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)
    logo = models.ImageField(null=True, blank=True, default='/placeholder.png')
    about = models.TextField(max_length=500)
    tag = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    website = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-name',)