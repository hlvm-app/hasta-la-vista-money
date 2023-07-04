from config.django.forms import BaseForm, DateTimePickerWidgetForm
from django.utils.translation import gettext_lazy as _
from hasta_la_vista_money.expense.models import Expense, ExpenseType


class AddExpenseForm(BaseForm):
    labels = {
        'category': _('Категория расхода'),
        'account': _('Счёт'),
        'date': _('Дата'),
        'amount': _('Сумма'),
    }

    class Meta:
        model = Expense
        fields = ['category', 'account', 'date', 'amount']
        widgets = {
            'date': DateTimePickerWidgetForm,
        }


class AddCategoryForm(BaseForm):
    labels = {
        'name': 'Название категории',
    }

    class Meta:
        model = ExpenseType
        fields = ['name']
