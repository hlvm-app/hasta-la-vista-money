from django.contrib.auth.models import AbstractUser
from django.db import models
from hasta_la_vista_money.constants import NumericParameter

CURRENCY = (
    ('RU', 'Российский рубль'),
)


class User(AbstractUser):
    def __str__(self):
        return self.username


class TelegramUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(
        max_length=NumericParameter.TWO_HUNDRED_FIFTY.value,
    )
    telegram_id = models.BigIntegerField(unique=True)


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name_account = models.CharField(
        max_length=NumericParameter.TWO_HUNDRED_FIFTY.value,
        default='Основной счёт',
    )
    balance = models.DecimalField(
        max_digits=NumericParameter.TWENTY.value,
        decimal_places=2,
        default=0,
    )
    currency = models.CharField(choices=CURRENCY)

    def __str__(self):
        return self.name_account
