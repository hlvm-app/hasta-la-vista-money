import decimal

from django.db import models
from django.urls import reverse
from hasta_la_vista_money import constants
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.users.models import User


class Loan(models.Model):
    TYPE_LOAN = [
        ('Annuity', 'Аннуитетный'),
        ('Differentiated', 'Дифференцированный'),
    ]

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
        max_length=constants.TWO_HUNDRED_FIFTY,
    )
    annual_interest_rate = models.DecimalField(
        max_digits=constants.TWO_HUNDRED_FIFTY,
        decimal_places=constants.TWO,
    )
    period_loan = models.IntegerField()
    type_loan = models.CharField(choices=TYPE_LOAN, default=TYPE_LOAN[0][0])

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
            loan_id=self.id,
        ).aggregate(models.Sum('monthly_payment'))

        total_monthly_payment = monthly_payment.get(
            'monthly_payment__sum',
        ) or decimal.Decimal('0.00')

        if self.loan_amount:
            return total_monthly_payment - decimal.Decimal(self.loan_amount)

        return total_monthly_payment

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
        max_digits=constants.TWO_HUNDRED_FIFTY,
        decimal_places=constants.TWO,
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
        max_digits=constants.SIXTY,
        decimal_places=constants.TWO,
    )
    monthly_payment = models.DecimalField(
        max_digits=constants.SIXTY,
        decimal_places=constants.TWO,
    )
    interest = models.DecimalField(
        max_digits=constants.SIXTY,
        decimal_places=constants.TWO,
    )
    principal_payment = models.DecimalField(
        max_digits=constants.SIXTY,
        decimal_places=constants.TWO,
    )
