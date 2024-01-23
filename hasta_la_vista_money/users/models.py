from django.contrib.auth.models import AbstractUser
from django.db import models
from hasta_la_vista_money import constants


class User(AbstractUser):
    def __str__(self):
        return self.username


class TelegramUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='telegram_users',
    )
    username = models.CharField(
        max_length=constants.TWO_HUNDRED_FIFTY,
    )
    telegram_id = models.BigIntegerField(unique=True)
    selected_account = models.ForeignKey(
        'account.Account',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='selected_account_telegram_users',
    )
