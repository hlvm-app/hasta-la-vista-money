from django.db import models
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.constants import NumericParameter
from hasta_la_vista_money.users.models import User


class ExpenseType(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=NumericParameter.TWO_HUNDRED_FIFTY.value)

    def __str__(self):
        return str(self.name)


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    category = models.ForeignKey(ExpenseType, on_delete=models.PROTECT)
    date = models.DateTimeField()
    amount = models.DecimalField(
        null=True,
        max_digits=NumericParameter.TWENTY.value,
        decimal_places=NumericParameter.TWO.value,
    )

    def __str__(self):
        return str(self.category)
