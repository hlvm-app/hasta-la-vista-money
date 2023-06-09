from django.db import models

from hasta_la_vista_money.users.models import Account, User

CATEGORIES = (
    ('ЖКХ', 'ЖКХ'),
)


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    category = models.CharField(max_length=20, choices=CATEGORIES)
    description = models.CharField(max_length=250)
