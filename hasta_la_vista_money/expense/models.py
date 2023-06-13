from django.db import models
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.constants import NumericParameter
from hasta_la_vista_money.users.models import User

CATEGORIES = (
    ('ЖКХ', 'ЖКХ'),
)


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    name = models.CharField(max_length=NumericParameter.ONE_HUNDRED.value)
    date = models.DateTimeField()
    category = models.CharField(
        max_length=NumericParameter.TWENTY.value, choices=CATEGORIES,
    )
    description = models.CharField(
        max_length=NumericParameter.TWO_HUNDRED_FIFTY.value,
    )
