from config.django.forms import BaseForm
from django.utils.translation import gettext_lazy as _
from hasta_la_vista_money.income.models import Income


class IncomeForm(BaseForm):
    """Модельная форма отображения доходов на сайте."""

    labels = {
        'type_income': _('Тип дохода'),
        'month': _('Месяц'),
        'amount': _('Сумма'),
    }

    class Meta:
        model = Income
        fields = ['type_income', 'month', 'amount']
