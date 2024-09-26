from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Create your models here.
class User(AbstractUser):
    email_active = models.CharField(max_length=72, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    def __str__(self):

        if self.first_name != "" and self.last_name != "":
            return self.get_full_name()
        return self.email



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True,null=True, blank=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(auto_now=True)

    def otp_is_valid(self):
        # اعتبارسنجی کد OTP بر اساس زمان
        now = timezone.now()
        return (now - self.otp_created_at).seconds < 300
