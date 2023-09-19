from django.db import models
from hasta_la_vista_money.constants import NumericParameter
from hasta_la_vista_money.users.models import User

CURRENCY = (('RU', 'Российский рубль'),)


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
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

    def __str__(self):
        return f'{self.name_account}'

    def transfer_money(self, to_account, amount):
        if amount <= self.balance:
            self.balance -= amount  # noqa: WPS601
            to_account.balance += amount
            self.save()
            to_account.save()
            return True
        return False


class TransferMoneyLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    exchange_date = models.DateTimeField()

    def __str__(self):
        return f'Перевод со счёта {self.from_account} на счёт {self.to_account}'
