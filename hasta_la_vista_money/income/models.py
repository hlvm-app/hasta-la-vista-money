from datetime import datetime

from django.db import models
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.constants import NumericParameter
from hasta_la_vista_money.users.models import User

TYPE_INCOME = (
    ('Зарплата', 'Зарплата'),
    ('Алименты', 'Алименты'),
    ('Возврат денег (Налог, покупка)', 'Возврат денег (Налог, покупка)'),
    ('Доход от аренды', 'Доход от аренды'),
    ('Дивиденды', 'Дивиденды'),
    ('Кредит', 'Кредит'),
    ('Лотереи (Азартные игры)', 'Лотереи (Азартные игры)'),
    ('Подарки', 'Подарки'),
    ('Продажа', 'Продажа'),
    ('Членские взносы и гранды', 'Членские взносы и гранды'),
)

current_year = datetime.now().year


class Income(models.Model):
    """Модель доходов."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    type_income = models.CharField(
        max_length=NumericParameter.TWO_HUNDRED_FIFTY.value,
        choices=TYPE_INCOME,
    )
    date = models.DateTimeField()
    amount = models.DecimalField(
        max_digits=NumericParameter.TWENTY.value, decimal_places=2,
    )

    def __str__(self):
        return self.type_income
