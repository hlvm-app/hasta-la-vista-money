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

    def __init__(self, user, *args, **kwargs):
        """Фильтруем категории по пользователям."""
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['category'].queryset = IncomeType.objects.filter(user=user)

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
