from django.db import models
from hasta_la_vista_money import constants
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.commonlogic.models import CommonIncomeExpense
from hasta_la_vista_money.users.models import CustomUser


class ExpenseCategory(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='category_expense_users',
    )
    name = models.CharField(
        max_length=constants.TWO_HUNDRED_FIFTY,
        unique=True,
    )
    parent_category = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='subcategories',
        on_delete=models.PROTECT,
    )

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return str(self.name)


class Expense(CommonIncomeExpense):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='expense_users',
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='expense_accounts',
    )
    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.PROTECT,
        related_name='expense_categories',
    )

    def __str__(self):
        return str(self.category)
