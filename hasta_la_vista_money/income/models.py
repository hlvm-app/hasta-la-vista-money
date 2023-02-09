from django.db import models


salary = (
    ('Зарплата', 'Зарплата'),
)

months = (
    ('Январь', 'Январь'),
    ('Февраль', 'Февраль'),
    ('Март', 'Март'),
    ('Апрель', 'Апрель'),
    ('Май', 'Май'),
    ('Июнь', 'Июнь'),
    ('Июль', 'Июль'),
    ('Август', 'Август'),
    ('Сентябрь', 'Сентябрь'),
    ('Октябрь', 'Месяц'),
    ('Ноябрь', 'Ноябрь'),
    ('Декабрь', 'Декабрь'),
)


class Income(models.Model):
    type_income = models.CharField(max_length=10, choices=salary)
    month = models.CharField(max_length=10, choices=months)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.type_income
