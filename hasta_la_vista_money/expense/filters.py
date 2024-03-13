import django_filters
from django.forms import Select
from django.utils.translation import gettext_lazy as _

from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.expense.models import Expense, ExpenseCategory


class ExpenseFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(
        queryset=ExpenseCategory.objects.all(),
        field_name='category',
        label=_('Категория'),
        widget=Select(attrs={'class': 'form-control mb-2'}),
    )
    date = django_filters.DateFromToRangeFilter(
        label=_('Период'),
        widget=django_filters.widgets.RangeWidget(
            attrs={
                'class': 'form-control',
                'type': 'date',
            },
        ),
    )
    account = django_filters.ModelChoiceFilter(
        queryset=Account.objects.all(),
        label=_('Счёт'),
        widget=Select(attrs={'class': 'form-control mb-4'}),
    )

    def __init__(self, *args, **kwargs):
        """
        Конструктор класса инициализирующий поля формы.

        :param args:
        :param kwargs:
        """
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.filters['category'].queryset = (
            ExpenseCategory.objects.filter(user=self.user)
            .distinct()
            .order_by('name')
        )
        self.filters['account'].queryset = Account.objects.filter(
            user=self.user,
        )

    @property
    def qs(self):
        queryset = super().qs
        if self.user:
            queryset = queryset.filter(user=self.user).distinct()
        category_filter = self.form.cleaned_data.get('category')
        if category_filter:
            queryset = (
                queryset.filter(
                    user=self.user,
                    category=category_filter,
                )
                .distinct()
                .values(
                    'id',
                    'date',
                    'account__name_account',
                    'category__name',
                    'category__parent_category__name',
                    'amount',
                )
            )

        account_filter = self.form.cleaned_data.get('account')
        queryset = (
            queryset.filter(
                user=self.user,
                account=account_filter,
            )
            .distinct()
            .values(
                'id',
                'date',
                'account__name_account',
                'category__name',
                'category__parent_category__name',
                'amount',
            )
        )
        return queryset

    class Meta:
        model = Expense
        fields = ['category', 'date', 'account']
