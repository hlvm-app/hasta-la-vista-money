import decimal

from django.db import models
from django.urls import reverse
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.constants import NumericParameter
from hasta_la_vista_money.users.models import User


class Loan(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='loan_users',
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='loan_accounts',
    )
    date = models.DateTimeField()
    loan_amount = models.FloatField(
        max_length=NumericParameter.TWO_HUNDRED_FIFTY.value,
    )
    annual_interest_rate = models.DecimalField(
        max_digits=NumericParameter.TWO_HUNDRED_FIFTY.value,
        decimal_places=NumericParameter.TWO.value,
    )
    period_loan = models.IntegerField()

    class Meta:
        ordering = ['-id']
        indexes = [
            models.Index(fields=['-id']),
            models.Index(fields=['loan_amount']),
            models.Index(fields=['annual_interest_rate']),
            models.Index(fields=['period_loan']),
        ]

    def __str__(self):
        return f'Кредит №{self.id} на сумму {self.loan_amount}'

    def get_absolute_url(self):
        return reverse('loan:delete', args=[self.id])

    @property
    def calculate_sum_monthly_payment(self):
        monthly_payment = PaymentSchedule.objects.filter(
            user=self.user,
        ).aggregate(models.Sum('monthly_payment'))
        return monthly_payment.get('monthly_payment__sum') - decimal.Decimal(
            self.loan_amount,
        )

    @property
    def calculate_total_amount_loan_with_interest(self):
        sum_monthly_payment = self.calculate_sum_monthly_payment
        return decimal.Decimal(self.loan_amount) + sum_monthly_payment


class PaymentMakeLoan(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='payment_make_loan_users',
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='payment_make_loan_accounts',
    )
    date = models.DateTimeField()
    loan = models.ForeignKey(
        Loan,
        on_delete=models.CASCADE,
        related_name='loans',
    )
    amount = models.DecimalField(
        max_digits=NumericParameter.TWO_HUNDRED_FIFTY.value,
        decimal_places=NumericParameter.TWO.value,
    )


class PaymentSchedule(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='payment_schedule_users',
    )
    loan = models.ForeignKey(
        Loan,
        on_delete=models.CASCADE,
        related_name='payment_schedule_loans',
    )
    date = models.DateTimeField()
    balance = models.DecimalField(
        max_digits=NumericParameter.SIXTY.value,
        decimal_places=NumericParameter.TWO.value,
    )
    monthly_payment = models.DecimalField(
        max_digits=NumericParameter.SIXTY.value,
        decimal_places=NumericParameter.TWO.value,
    )
    interest = models.DecimalField(
        max_digits=NumericParameter.SIXTY.value,
        decimal_places=NumericParameter.TWO.value,
    )
    principal_payment = models.DecimalField(
        max_digits=NumericParameter.SIXTY.value,
        decimal_places=NumericParameter.TWO.value,
    )
