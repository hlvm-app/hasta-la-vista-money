from django.db import models
from hasta_la_vista_money.constants import NumericParameter


class CommonIncomeExpense(models.Model):
    date = models.DateTimeField()
    amount = models.DecimalField(
        max_digits=NumericParameter.TWENTY.value,
        decimal_places=2,
    )

    class Meta:
        abstract = True
        ordering = ['-date']
        indexes = [
            models.Index(fields=['-date']),
            models.Index(fields=['amount']),
        ]

    def __str__(self):
        return str(self.category)
