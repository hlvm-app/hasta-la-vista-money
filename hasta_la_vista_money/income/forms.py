from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from config.django.forms import BaseForm
from django.utils.translation import gettext_lazy as _
from hasta_la_vista_money.income.models import Income, IncomeType


class IncomeForm(BaseForm):
    """Модельная форма отображения доходов на сайте."""

    labels = {
        'category': _('Категория дохода'),
        'date': _('Дата'),
        'amount': _('Сумма'),
        'account': _('Счёт'),
    }

    class Meta:
        model = Income
        fields = ['category', 'date', 'amount', 'account']
        widgets = {
            'date': DateTimePickerInput(
                options={
                    'format': 'DD/MM/YYYY HH:ss',
                    'showTodayButton': True,
                },
            ),
        }


class AddCategoryIncomeForm(BaseForm):
    labels = {
        'name': 'Название категории',
    }

    class Meta:
        model = IncomeType
        fields = ['name']
