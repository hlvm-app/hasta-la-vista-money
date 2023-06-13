from datetime import datetime

from django.db import models
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.constants import NumericParameter
from hasta_la_vista_money.users.models import User


class IncomeType(models.Model):
    name = models.CharField(max_length=NumericParameter.TWO_HUNDRED_FIFTY.value)

    def __str__(self):
        return self.name


class Income(models.Model):
    """Модель доходов."""

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    type_income = models.ForeignKey(IncomeType, on_delete=models.PROTECT)
    date = models.DateTimeField()
    amount = models.DecimalField(
        max_digits=NumericParameter.TWENTY.value, decimal_places=2,
    )

    def __str__(self):
        return self.type_income



