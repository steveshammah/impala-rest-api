from django.db import models
from django.contrib.auth.models import User

class SmsModel(models.Model):
    """
    SMS Model to handle SIM verification

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    counter = models.PositiveIntegerField(default=0, blank=False)
    isVerified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.telephone


class NotificationModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_content = models.TextField()
    notification_read = models.BooleanField(default=0)

