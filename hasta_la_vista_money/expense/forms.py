from config.django.forms import BaseForm, DateTimePickerWidgetForm
from django.utils.translation import gettext_lazy as _
from hasta_la_vista_money.expense.models import Expense, ExpenseType


class AddExpenseForm(BaseForm):
    labels = {
        'category': _('Категория расхода'),
        'account': _('Счёт списания'),
        'date': _('Дата'),
        'amount': _('Сумма'),
    }

    def __init__(self, user, *args, **kwargs):
        """Фильтруем категории по пользователям."""
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['category'].queryset = ExpenseType.objects.filter(user=user)

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
