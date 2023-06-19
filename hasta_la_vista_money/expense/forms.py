from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from config.django.forms import BaseForm
from django.utils.translation import gettext_lazy as _
from hasta_la_vista_money.expense.models import Expense


class AddExpenseForm(BaseForm):
    labels = {
        'account': _('Счёт'),
        'category': _('Категория'),
        'date': _('Дата'),
        'amount': _('Сумма'),
    }

    class Meta:
        model = Expense
        fields = ['account', 'category', 'date', 'amount']
        widgets = {
            'date': DateTimePickerInput(
                options={
                    'format': 'DD/MM/YYYY HH:ss',
                    'showTodayButton': True,
                },
            ),
        }
