from datetime import datetime

from django.db import models
from hasta_la_vista_money.constants import NumericParameter
from hasta_la_vista_money.users.models import Account, User

salary = (
    ('Зарплата', 'Зарплата'),
)

current_year = datetime.now().year


months = (
    (f'Январь {current_year}', f'Январь {current_year}'),
    (f'Февраль {current_year}', f'Февраль {current_year}'),
    (f'Март {current_year}', f'Март {current_year}'),
    (f'Апрель {current_year}', f'Апрель {current_year}'),
    (f'Май {current_year}', f'Май {current_year}'),
    (f'Июнь {current_year}', f'Июнь {current_year}'),
    (f'Июль {current_year}', f'Июль {current_year}'),
    (f'Август {current_year}', f'Август {current_year}'),
    (f'Сентябрь {current_year}', f'Сентябрь {current_year}'),
    (f'Октябрь {current_year}', f'Октябрь {current_year}'),
    (f'Ноябрь {current_year}', f'Ноябрь {current_year}'),
    (f'Декабрь {current_year}', f'Декабрь {current_year}'),
)


class Income(models.Model):
    """Модель доходов."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    type_income = models.CharField(
        max_length=NumericParameter.TWENTY.value, choices=salary,
    )
    date = models.DateTimeField()
    amount = models.DecimalField(
        max_digits=NumericParameter.TWENTY.value, decimal_places=2,
    )

    def __str__(self):
        return self.type_income
