from django.db import models
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.constants import NumericParameter
from hasta_la_vista_money.users.models import User


class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    date = models.DateTimeField()
    loan_amount = models.FloatField(
        max_length=NumericParameter.TWO_HUNDRED_FIFTY.value,
    )
    annual_interest_rate = models.DecimalField(
        max_digits=NumericParameter.TWO_HUNDRED_FIFTY.value,
        decimal_places=NumericParameter.TWO.value,
    )
    period_loan = models.IntegerField(
        max_length=NumericParameter.TWO_HUNDRED_FIFTY.value,
    )


class PaymentMakeLoan(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    loan = models.ForeignKey(Loan, on_delete=models.PROTECT)
    amount = models.DecimalField(
        max_digits=NumericParameter.TWO_HUNDRED_FIFTY.value,
        decimal_places=NumericParameter.TWO.value,
    )
