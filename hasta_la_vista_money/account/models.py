from datetime import datetime

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from hasta_la_vista_money.constants import NumericParameter
from hasta_la_vista_money.users.models import User


class Account(models.Model):
    CURRENCY = [('RU', _('Российский рубль'))]

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='account_users',
    )
    name_account = models.CharField(
        max_length=NumericParameter.TWO_HUNDRED_FIFTY.value,
        default='Основной счёт',
    )
    balance = models.DecimalField(
        max_digits=NumericParameter.TWENTY.value,
        decimal_places=2,
        default=0,
    )
    currency = models.CharField(choices=CURRENCY)

    class Meta:
        ordering = ['name_account']
        indexes = [models.Index(fields=['name_account'])]

    def __str__(self):
        return f'{self.name_account}'

    def get_absolute_url(self):
        return reverse('account:change', args=[self.id])

    def transfer_money(self, to_account, amount):
        if amount <= self.balance:
            self.balance -= amount  # noqa: WPS601
            to_account.balance += amount
            self.save()
            to_account.save()
            return True
        return False


class TransferMoneyLog(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transfer_money',
    )
    from_account = models.ForeignKey(
        Account,
        related_name='from_account',
        on_delete=models.CASCADE,
    )
    to_account = models.ForeignKey(
        Account,
        related_name='to_account',
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        max_digits=NumericParameter.TWENTY.value,
        decimal_places=NumericParameter.TWO.value,
    )
    exchange_date = models.DateTimeField(default=datetime.now)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ['-exchange_date']

    def __str__(self):
        return ''.join(
            (
                f'{self.exchange_date:%d-%m-%Y %H:%M}. ',
                f'Перевод суммы {self.amount} ',
                f'со счёта "{self.from_account}" на счёт "{self.to_account}". ',
            ),
        )
