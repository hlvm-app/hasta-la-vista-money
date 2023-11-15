from django.forms import ModelChoiceField
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from hasta_la_vista_money.commonlogic.forms import (
    BaseForm,
    DateTimePickerWidgetForm,
    get_category_choices,
)
from hasta_la_vista_money.income.models import Income, IncomeCategory
from hasta_la_vista_money.users.models import User


class IncomeForm(BaseForm):
    """Модельная форма отображения доходов на сайте."""

    labels = {
        'category': _('Категория дохода'),
        'account': _('Счёт начисления'),
        'date': _('Дата'),
        'amount': _('Сумма'),
    }

    category = ModelChoiceField(queryset=IncomeCategory.objects.all())

    def __init__(self, user, depth, *args, **kwargs):
        """Конструктор формы."""
        super().__init__(*args, **kwargs)
        user = get_object_or_404(User, username=user)
        categories = (
            user.category_income_users.select_related('user')
            .order_by('parent_category_id')
            .all()
        )
        category_choices = get_category_choices(
            queryset=categories,
            max_level=depth,
        )
        self.fields['category'].choices = category_choices

    class Meta:
        model = Income
        fields = ['category', 'account', 'date', 'amount']
        widgets = {
            'date': DateTimePickerWidgetForm,
        }


class AddCategoryIncomeForm(BaseForm):
    labels = {
        'name': 'Название категории',
        'parent_category': 'Вложенность',
    }

    def __init__(self, user, depth, *args, **kwargs):
        """Конструктор формы."""
        super().__init__(*args, **kwargs)
        user = get_object_or_404(User, username=user)
        categories = (
            user.category_income_users.select_related('user')
            .order_by('parent_category_id')
            .all()
        )
        category_choices = get_category_choices(
            queryset=categories,
            max_level=depth,
        )
        self.fields['parent_category'].choices = category_choices

    class Meta:
        model = IncomeCategory
        fields = ['name', 'parent_category']
