from datetime import datetime

from django.db import models

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
    type_income = models.CharField(max_length=10, choices=salary)
    month = models.CharField(max_length=20, choices=months)
    amount = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return self.type_income
