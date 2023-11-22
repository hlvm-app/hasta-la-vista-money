from django.db import models
from hasta_la_vista_money.users.models import User


class DateList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='budget_date_list_users',
    )
    date = models.DateTimeField()


class Planning(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='budget_category_users',
    )
