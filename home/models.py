from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import date


class Author(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default="", upload_to='uploads/', null=True, blank=True)
    phone = models.CharField(max_length=100, default="")
    is_editor = models.BooleanField(default=0)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ('-user',)


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
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=100)
    profile_pic = models.ImageField(default="", upload_to='uploads/', null=True, blank=True)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL)
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


class Tag(models.Model):
    tag = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.tag


class Article(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    headline = models.CharField(max_length=250)
    content_1 = models.TextField(max_length=None)
    content_2 = models.TextField(max_length=None, null=True)
    image_1 = models.ImageField(upload_to='uploads/', null=True, blank=True)
    caption_1 = models.CharField(max_length=250, null=True, default='Impala Rugby')
    image_2 = models.ImageField(upload_to='uploads/', null=True, blank=True)
    caption_2 = models.CharField(max_length=250, null=True, default='Impala Rugby')
    type = models.CharField(max_length=100, null=True, default='article')
    tags = models.CharField(max_length=150, null=True, default='Impala')
    created = models.DateTimeField(auto_now_add=True)
    posted = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title


class Product(models.Model):
    PRODUCT_TYPE = [
        ("J", "Jersey"),
        ("H", "Hoodies"),
        ("T", "T-shirt"),
        ("S", "Sweat-gear"),
        ("W", "Water-bottle"),
    ]
    product_name = models.CharField(
        choices=PRODUCT_TYPE, max_length=150, blank=True, null=True
    )
    image = models.ImageField(null=True, blank=True, default='/placeholder.png')
    price = models.IntegerField()
    description = models.TextField(max_length=500)
    color = models.CharField(max_length=100, blank=True, null=True)
    count_in_stock = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    class Meta:
        ordering = ('-product_name',)


class Fixture(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_team', default='1')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_team', default='1')
    match_date = models.DateField(None)
    venue = models.CharField(max_length=100)
    kickoff = models.CharField(max_length=20)

    def clean(self):
        if self.home_team == self.away_team:
            raise ValidationError("Home team cannot be similar to the Away team.")


class Partner(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)
    logo = models.ImageField(null=True, blank=True, default='/placeholder.png')
    about = models.TextField(max_length=500)
    tag = models.CharField(max_length=200, null=True, blank=True)
    url = models.CharField(max_length=100, null=True, blank=True)
    website = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-name',)


class SmsModel(models.Model):
    """
    SMS Model to handle SIM verification

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    counter = models.IntegerField(default=0, blank=False)
    isVerified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.telephone


class NotificationModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_content = models.TextField()
    notification_read = models.BooleanField(default=0)


class FixtureResult(models.Model):
    fixture = models.ForeignKey(Fixture, on_delete=models.CASCADE)
    fixture_results = models.CharField(max_length=100)
    MOTM = models.CharField(max_length=20, blank=True, null=True)


# class MatchdaySquad(models.Model):
#     pass
