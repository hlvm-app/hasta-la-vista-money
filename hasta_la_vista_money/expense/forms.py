from django.forms import DateTimeInput, ModelChoiceField
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.commonlogic.forms import (
    BaseForm,
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

    category = ModelChoiceField(queryset=ExpenseCategory.objects.all())

    def __init__(self, user, depth, *args, **kwargs):
        """Конструктор формы."""
        self.user = user
        super().__init__(*args, **kwargs)
        selected_user = get_object_or_404(User, username=self.user)
        categories = (
            selected_user.category_expense_users.select_related('user')
            .order_by('parent_category__name', 'name')
            .all()
        )
        category_choices = get_category_choices(
            queryset=categories,
            max_level=depth,
        )
        category_choices.insert(0, ('', '----------'))
        self.fields['category'].choices = category_choices

    def clean(self):
        cleaned_data = super().clean()
        account_form = cleaned_data.get('account')
        amount = cleaned_data.get('amount')
        category = cleaned_data.get('category')

        if account_form and amount and category:
            account = get_object_or_404(Account, id=account_form.id)
            if amount > account.balance:
                self.add_error(
                    'account',
                    f'Недостаточно средств на счёте {account}',
                )
        return cleaned_data

    class Meta:
        model = Expense
        fields = ['category', 'account', 'date', 'amount']
        widgets = {
            'date': DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'},
            ),
        }


class AddCategoryForm(BaseForm):
    labels = {
        'name': 'Название категории',
        'parent_category': 'Вложенность',
    }

    def __init__(self, user, depth, *args, **kwargs):
        """Конструктор формы."""
        super().__init__(*args, **kwargs)
        current_user = get_object_or_404(User, username=user)
        categories = (
            current_user.category_expense_users.select_related('user')
            .order_by('parent_category_id')
            .all()
        )
        category_choices = get_category_choices(
            queryset=categories,
            max_level=depth,
        )
        category_choices.insert(0, ('', '----------'))
        self.fields['parent_category'].choices = category_choices

    class Meta:
        model = ExpenseCategory
        fields = ['name', 'parent_category']
