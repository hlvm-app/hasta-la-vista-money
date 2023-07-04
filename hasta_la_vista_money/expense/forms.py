import datetime

from django.utils import timezone

from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from config.django.forms import BaseForm
from django.utils.translation import gettext_lazy as _

from hasta_la_vista_money import constants
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
            'date': DateTimePickerInput(
                options={
                    'format': 'DD/MM/YYYY HH:mm',
                    'showTodayButton': True,
                    'minDate': (
                            constants.TODAY.replace(
                                month=1, day=1, year=constants.TODAY.year - 1
                            ) - datetime.timedelta(days=1826)
                    ).strftime('%d/%m/%Y %H:%M'),
                    'maxDate': constants.TODAY.replace(
                        hour=23, minute=59, second=59
                    )
                },
            ),
        }


class AddCategoryForm(BaseForm):
    labels = {
        'name': 'Название категории',
    }

    class Meta:
        model = ExpenseType
        fields = ['name']
