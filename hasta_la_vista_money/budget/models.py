from django.db import models
from hasta_la_vista_money.users.models import User


class DateList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='budget_date_list_users',
    )
    date = models.DateTimeField()
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        verbose_name='Date created',
    )


class Planning(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='budget_category_users',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        verbose_name='Date created',
    )
