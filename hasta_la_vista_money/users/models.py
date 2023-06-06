from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

CURRENCY = (
    ('RU', 'Российский рубль'),
)


class User(AbstractUser):
    def __str__(self):
        return self.username


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name_account = models.CharField(max_length=250, default='Основной счёт')
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    currency = models.CharField(choices=CURRENCY)
