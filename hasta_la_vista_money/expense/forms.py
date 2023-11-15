from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.commonlogic.forms import (
    BaseForm,
    DateTimePickerWidgetForm,
    get_category_choices,
)
from hasta_la_vista_money.expense.models import Expense, ExpenseCategory
from hasta_la_vista_money.users.models import User


class AddExpenseForm(BaseForm):
    labels = {
        'category': _('Категория расхода'),
        'account': _('Счёт списания'),
        'date': _('Дата'),
        'amount': _('Сумма'),
    }

    class Meta:
        model = Expense
        fields = ['category', 'account', 'date', 'amount']
        widgets = {
            'date': DateTimePickerWidgetForm,
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
        self.fields['category'].choices = category_choices

    def clean(self):
        cleaned_data = super().clean()
        account = cleaned_data.get('account')
        amount = cleaned_data.get('amount')
        if account:
            account = get_object_or_404(Account, name_account=account)
            if amount > account.balance:
                self.add_error(
                    'account',
                    f'Недостаточно средств на счёте {account}',
                )
            return cleaned_data


class AddCategoryForm(BaseForm):
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
        model = ExpenseCategory
        fields = ['name', 'parent_category']
