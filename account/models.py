from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    email_active = models.CharField(max_length=72,null=True,blank=True)
    avatar = models.ImageField(upload_to='avatars',null=True,blank=True)
    phone_number = models.CharField(max_length=11)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
