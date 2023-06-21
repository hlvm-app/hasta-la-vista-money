from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from hasta_la_vista_money.constants import (
    CURRENT_YEAR,
    MONTH_NAMES,
    MONTH_NUMBERS,
    NumberMonthOfYear,
)
from hasta_la_vista_money.custom_mixin import CustomNoPermissionMixin
from hasta_la_vista_money.expense.models import Expense
from hasta_la_vista_money.income.models import Income


class ReportView(CustomNoPermissionMixin, SuccessMessageMixin, TemplateView):
    template_name = 'reports/reports.html'
    no_permission_url = reverse_lazy('login')
    success_url = reverse_lazy('reports:list')

    @classmethod
    def format_month_year(cls, dt):
        month_number = dt.month
        month_name = list(MONTH_NUMBERS.keys())[
            list(MONTH_NUMBERS.values()).index(month_number)
        ]
        year = dt.year
        return f'{month_name} {year}'

    @classmethod
    def get_month_total_amount_income(cls, request):
        return Income.objects.filter(
            user=request.user,
        ).values('date', 'account').annotate(
            total_amount=Sum('amount'),
        )

    @classmethod
    def get_month_total_amount_expense(cls, request):
        return Expense.objects.filter(
            user=request.user,
        ).values('date', 'account').annotate(
            total_amount=Sum('amount'),
        )

    @classmethod
    def get_list_months_year(cls):
        months_year = []
        for month in range(  # noqa: WPS352
            NumberMonthOfYear.NUMBER_FIRST_MONTH_YEAR.value,
            NumberMonthOfYear.NUMBER_TWELFTH_MONTH_YEAR.value + 1,
        ):
            month_name = MONTH_NAMES.get(month, 'Неизвестно')
            months_year.append(f'{month_name} {CURRENT_YEAR}')

        # Сортировка списка месяцев
        months_year.sort(
            key=lambda months: MONTH_NUMBERS.get(months.split()[0], 0),
        )
        return months_year

    def get(self, request, *args, **kwargs):
        if request.user:
            income_amounts = {
                self.format_month_year(income_dict['date']):
                    income_dict['total_amount']
                for income_dict in self.get_month_total_amount_income(request)
            }

            expense_amounts = {
                self.format_month_year(expense_dict['date']):
                    expense_dict['total_amount']
                for expense_dict in self.get_month_total_amount_expense(request)
            }

            # Создание списков сумм доходов/чеков в правильном порядке
            income_amounts = [
                float(income_amounts.get(
                    month_year, 0,
                ),
                ) for month_year in self.get_list_months_year()
            ]

            expense_amounts = [
                float(expense_amounts.get(
                    month_year, 0,
                ),
                ) for month_year in self.get_list_months_year()
            ]

            return render(request, self.template_name, {
                'income_amounts': income_amounts,
                'expense_amounts': expense_amounts,
            })
