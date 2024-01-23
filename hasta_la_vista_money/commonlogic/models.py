from django.db import models
from hasta_la_vista_money import constants


class CommonIncomeExpense(models.Model):
    date = models.DateTimeField()
    amount = models.DecimalField(
        max_digits=constants.TWENTY,
        decimal_places=2,
    )

    class Meta:
        abstract = True
        ordering = ['-date']
        indexes = [
            models.Index(fields=['-date']),
            models.Index(fields=['amount']),
        ]
