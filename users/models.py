from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class Admin(AbstractBaseUser):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=100)
    USERNAME_FIELD = 'username'
