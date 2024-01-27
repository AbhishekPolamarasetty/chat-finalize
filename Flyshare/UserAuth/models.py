from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

# Create your models here.

class UserModel(AbstractUser):

    username = models.CharField(max_length=255,unique = True,default='default_username')
    email = models.EmailField(unique = True)
    phone_number = models.CharField(max_length=10)
    # if method =='PUT':
    #     email = models.EmailField()
    #     phone_number = models.CharField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    class Meta:
        swappable = 'AUTH_USER_MODEL'