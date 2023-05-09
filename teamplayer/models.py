from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date

class Team(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)
    logo = models.ImageField(null=True, blank=True, default='/placeholder.png')
    description = models.TextField(max_length=500)
    home_ground = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    league = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=100)
    profile_pic = models.ImageField(
        default="", upload_to='uploads/', null=True, blank=True)
    team = models.ForeignKey(
        Team, null=True, blank=True, on_delete=models.SET_NULL)
    social_link = models.CharField(max_length=150, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-user',)

    def __str__(self) -> str:
        return self.user.username

    def get_age(self):
        now = timezone.now
        today = date.today()
        one_or_zero = (today.month, today.day) < (
            self.date_of_birth.month,
            self.date_of_birth.day,
        )
        year_difference = today.year - self.date_of_birth.year
        age = year_difference - one_or_zero

        return age
