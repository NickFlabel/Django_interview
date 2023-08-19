from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    is_activated = models.BooleanField(default=False)
    activation_code = models.ForeignKey('InviteCode', related_name='users_activated', on_delete=models.SET_NULL, null=True)
    

class InviteCode(models.Model):

    invite_code = models.CharField(max_length=6, unique=True)
    user_owner = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='invite_code')

class PhoneCode(models.Model):

    user = models.OneToOneField('CustomUser', related_name='phone_code', on_delete=models.CASCADE)
    code = models.CharField(max_length=4, null=True, blank=True)

