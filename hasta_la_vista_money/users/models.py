from django.contrib import admin
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self) -> str:
        return self.username


class TokenAdmin(admin.ModelAdmin):  # type: ignore
    search_fields = ('key', 'user__username')
