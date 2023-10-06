from config.django.forms import BaseForm, DateTimePickerWidgetForm
from django.utils.translation import gettext_lazy as _
from hasta_la_vista_money.income.models import Income, IncomeType


class IncomeForm(BaseForm):
    """Модельная форма отображения доходов на сайте."""

    labels = {
        'category': _('Категория дохода'),
        'account': _('Счёт начисления'),
        'date': _('Дата'),
        'amount': _('Сумма'),
    }

    class Meta:
        model = Income
        fields = ['category', 'account', 'date', 'amount']
        widgets = {
            'date': DateTimePickerWidgetForm,
        }


class AddCategoryIncomeForm(BaseForm):
    labels = {
        'name': 'Название категории',
    }

    class Meta:
        model = IncomeType
        fields = ['name']
