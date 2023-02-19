from django.forms import ModelForm
from django.utils.translation import gettext_lazy

from hasta_la_vista_money.income.models import Income


class IncomeForm(ModelForm):
    class Meta:
        model = Income
        fields = ['type_income', 'month', 'amount']
        labels = {
            'type_income': gettext_lazy('Тип дохода'),
            'month': gettext_lazy('Месяц'),
            'amount': gettext_lazy('Сумма'),
        }
