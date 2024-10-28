from django.forms import DateTimeInput, ModelChoiceField
from django.utils.translation import gettext_lazy as _
from hasta_la_vista_money.commonlogic.forms import BaseForm
from hasta_la_vista_money.income.models import Income, IncomeCategory


class IncomeForm(BaseForm):
    """Модельная форма отображения доходов на сайте."""

    labels = {
        'category': _('Категория дохода'),
        'account': _('Счёт начисления'),
        'date': _('Дата'),
        'amount': _('Сумма'),
    }

    category = ModelChoiceField(queryset=IncomeCategory.objects.all())

    field = 'category'

    def configure_category_choices(self, category_choices):
        self.fields[self.field].choices = category_choices

    class Meta:
        model = Income
        fields = ['category', 'account', 'date', 'amount']
        widgets = {
            'date': DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'},
            ),
        }


class AddCategoryIncomeForm(BaseForm):
    labels = {
        'name': 'Название категории',
        'parent_category': 'Вложенность',
    }
    field = 'parent_category'

    class Meta:
        model = IncomeCategory
        fields = ['name', 'parent_category']

    def configure_category_choices(self, category_choices):
        self.fields[self.field].choices = category_choices
