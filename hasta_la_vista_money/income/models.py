from django.db import models
from django.urls import reverse
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.commonlogic.models import CommonIncomeExpense
from hasta_la_vista_money.constants import NumericParameter
from hasta_la_vista_money.users.models import User


class IncomeType(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='income_type',
    )
    name = models.CharField(max_length=NumericParameter.TWO_HUNDRED_FIFTY.value)

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]

    def __str__(self):
        return self.name


class Income(CommonIncomeExpense):
    """Модель доходов."""

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='income_users',
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='income_accounts',
    )
    category = models.ForeignKey(
        IncomeType,
        on_delete=models.PROTECT,
        related_name='income_categories',
    )

    def __str__(self):
        return str(self.category)

    def get_absolute_url(self):
        return reverse('income:change', args=[self.id])
