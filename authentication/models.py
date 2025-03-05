from django.db import models
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.models import User



# Create your models here.

class UserOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True)
    is_verified = models.BooleanField(default=False)  # Add this field

    def has_expired(self):
        if self.expires_at is None:
            return True
        return now() > self.expires_at
