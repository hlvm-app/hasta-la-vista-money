import json

from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from hasta_la_vista_money.custom_mixin import CustomNoPermissionMixin
from hasta_la_vista_money.expense.models import Expense
from hasta_la_vista_money.income.models import Income


class ReportView(CustomNoPermissionMixin, SuccessMessageMixin, TemplateView):
    template_name = 'reports/reports.html'
    no_permission_url = reverse_lazy('login')
    success_url = reverse_lazy('reports:list')

    @classmethod
    def collect_datasets(cls, request):
        expense_dataset = Expense.objects.filter(
            user=request.user,
        ).values(
            'date',
        ).annotate(
            total_amount=Sum('amount'),
        ).order_by('date')

        income_dataset = Income.objects.filter(
            user=request.user,
        ).values(
            'date',
        ).annotate(
            total_amount=Sum('amount'),
        ).order_by('date')

        return expense_dataset, income_dataset

    @classmethod
    def transform_data_expense(cls, expense_dataset):
        expense_dates = []
        expense_amounts = []

        for expense_date_amount in expense_dataset:
            expense_dates.append(
                expense_date_amount['date'].strftime('%Y-%m-%d'),
            )
            expense_amounts.append(float(expense_date_amount['total_amount']))

        return expense_dates, expense_amounts

    @classmethod
    def transform_data_income(cls, income_dataset):

        income_dates = []
        income_amounts = []

        for income_date_amount in income_dataset:
            income_dates.append(income_date_amount['date'].strftime('%Y-%m-%d'))
            income_amounts.append(float(income_date_amount['total_amount']))

        return income_dates, income_amounts

    @classmethod
    def unique_expense_data(cls, expense_dates, expense_amounts):
        unique_expense_dates = []
        unique_expense_amounts = []

        for expense_index, expense_date in enumerate(expense_dates):
            if expense_date not in unique_expense_dates:
                unique_expense_dates.append(expense_date)
                unique_expense_amounts.append(expense_amounts[expense_index])
            else:
                index = unique_expense_dates.index(expense_date)
                unique_expense_amounts[index] += expense_amounts[expense_index]

        return unique_expense_dates, unique_expense_amounts

    @classmethod
    def unique_income_data(cls, income_dates, income_amounts):
        unique_income_dates = []
        unique_income_amounts = []

        for income_index, income_date in enumerate(income_dates):
            if income_date not in unique_income_dates:
                unique_income_dates.append(income_date)
                unique_income_amounts.append(income_amounts[income_index])
            else:
                index = unique_income_dates.index(income_date)
                unique_income_amounts[index] += income_amounts[income_index]
        return unique_income_dates, unique_income_amounts

    def get(self, request, *args, **kwargs):  # noqa: WPS210 C901

        expense_dataset, income_dataset = self.collect_datasets(request)

        expense_dates, expense_amounts = self.transform_data_expense(
            expense_dataset,
        )
        income_dates, income_amounts = self.transform_data_income(
            income_dataset,
        )

        unique_expense_dates, unique_expense_amounts = self.unique_expense_data(
            expense_dates, expense_amounts,
        )

        unique_income_dates, unique_income_amounts = self.unique_income_data(
            income_dates, income_amounts,
        )

        chart = {
            'chart': {'type': 'line'},
            'title': {'text': 'Статистика по расходам и доходам'},
            'xAxis': [
                {'categories': unique_expense_dates,
                 'title': {'text': 'Дата (расходы)'},
                 },
                {'categories': unique_income_dates,
                 'title': {'text': 'Дата (доходы)'},
                 },
            ],
            'yAxis': {'title': {'text': 'Сумма'}},
            'series': [
                {
                    'name': 'Расходы',
                    'data': unique_expense_amounts,
                    'color': 'red',
                    'xAxis': 0,
                },
                {
                    'name': 'Доходы',
                    'data': unique_income_amounts,
                    'color': 'green',
                    'xAxis': 1,
                },
            ],
            'credits': {
                'enabled': False,
            },
            'exporting': {
                'enabled': False,
            },
        }

        dump = json.dumps(chart)

        return render(request, self.template_name, {'chart': dump})
