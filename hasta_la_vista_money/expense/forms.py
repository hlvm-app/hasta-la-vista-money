from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.commonlogic.forms import (
    BaseForm,
    DateTimePickerWidgetForm,
)
from hasta_la_vista_money.expense.models import Expense, ExpenseType


class AddExpenseForm(BaseForm):
    labels = {
        'category': _('Категория расхода'),
        'account': _('Счёт списания'),
        'date': _('Дата'),
        'amount': _('Сумма'),
    }

    class Meta:
        model = Expense
        fields = ['category', 'account', 'date', 'amount']
        widgets = {
            'date': DateTimePickerWidgetForm,
        }

    def clean(self):
        cleaned_data = super().clean()
        account = cleaned_data.get('account')
        amount = cleaned_data.get('amount')
        account_balance = get_object_or_404(Account, name_account=account)
        if amount > account_balance.balance:
            self.add_error(
                'account',
                f'Недостаточно средств на счёте {account}',
            )
        return cleaned_data


class AddCategoryForm(BaseForm):
    labels = {
        'name': 'Название категории',
    }

    class Meta:
        model = ExpenseType
        fields = ['name']
