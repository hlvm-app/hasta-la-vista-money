import json

from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from hasta_la_vista_money.custom_mixin import CustomNoPermissionMixin
from hasta_la_vista_money.expense.models import Expense
from hasta_la_vista_money.income.models import Income
from hasta_la_vista_money.users.forms import UpdateUserPasswordForm


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
    def transform_data(cls, dataset):
        dates = []
        amounts = []

        for date_amount in dataset:
            dates.append(
                date_amount['date'].strftime('%Y-%m-%d'),
            )
            amounts.append(float(date_amount['total_amount']))

        return dates, amounts

    @classmethod
    def transform_data_expense(cls, expense_dataset):
        return cls.transform_data(expense_dataset)

    @classmethod
    def transform_data_income(cls, income_dataset):
        return cls.transform_data(income_dataset)

    @classmethod
    def unique_data(cls, dates, amounts):
        unique_dates = []
        unique_amounts = []

        for data_index, date in enumerate(dates):
            if date not in unique_dates:
                unique_dates.append(date)
                unique_amounts.append(amounts[data_index])
            else:
                index = unique_dates.index(date)
                unique_amounts[index] += amounts[index]

        return unique_dates, unique_amounts

    @classmethod
    def unique_expense_data(cls, expense_dates, expense_amounts):
        return cls.unique_data(expense_dates, expense_amounts)

    @classmethod
    def unique_income_data(cls, income_dates, income_amounts):
        return cls.unique_data(income_dates, income_amounts)

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

        update_pass_user_form = UpdateUserPasswordForm(user=request.user)

        return render(
            request,
            self.template_name,
            {
                'chart': dump,
                'update_pass_user_form': update_pass_user_form,
            },
        )
