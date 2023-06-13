from django.contrib.humanize.templatetags.humanize import intcomma

from config.django.forms import BaseForm
from django import forms
from django.utils.translation import gettext_lazy as _
from hasta_la_vista_money.income.models import Income


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class IncomeForm(BaseForm):
    """Модельная форма отображения доходов на сайте."""

    labels = {
        'type_income': _('Тип дохода'),
        'date': _('Дата'),
        'amount': _('Сумма'),
        'account': _('Счёт'),
    }

    class Meta:
        model = Income
        fields = ['type_income', 'date', 'amount', 'account']
        widgets = {
            'date': DateTimeInput(),
        }
