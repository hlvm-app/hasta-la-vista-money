from django.contrib import admin
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self):
        return self.username


class TokenAdmin(admin.ModelAdmin):
    search_fields = ('key', 'user__username')
