import json

from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum
from django.db.models.functions import TruncMonth
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
        expense_dataset = (
            Expense.objects.filter(
                user=request.user,
            )
            .values(
                'date',
            )
            .annotate(
                total_amount=Sum('amount'),
            )
            .order_by('date')
        )

        income_dataset = (
            Income.objects.filter(
                user=request.user,
            )
            .values(
                'date',
            )
            .annotate(
                total_amount=Sum('amount'),
            )
            .order_by('date')
        )

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

    @classmethod
    def expense_category_month(cls, request):
        category_month = (
            Expense.objects.filter(user=request.user)  # noqa: WPS221
            .annotate(month=TruncMonth('date'))
            .values(
                'month',
                'category__parent_category__name',
            )
            .annotate(total_amount=Sum('amount'))
            .order_by(
                'month',
                'category__parent_category__name',
            )
        )

        grouped_category_month = {}
        for item in category_month:
            month_key = item['month']
            if month_key not in grouped_category_month:
                grouped_category_month[month_key] = []
            grouped_category_month[month_key].append(item)
        return grouped_category_month

    def get(self, request, *args, **kwargs):
        expense_dataset, income_dataset = self.collect_datasets(request)

        expense_dates, expense_amounts = self.transform_data_expense(
            expense_dataset,
        )
        income_dates, income_amounts = self.transform_data_income(
            income_dataset,
        )

        unique_expense_dates, unique_expense_amounts = self.unique_expense_data(
            expense_dates,
            expense_amounts,
        )

        unique_income_dates, unique_income_amounts = self.unique_income_data(
            income_dates,
            income_amounts,
        )

        chart_expense = {
            'chart': {'type': 'line'},
            'title': {'text': 'Статистика по расходам'},
            'xAxis': [
                {
                    'categories': unique_expense_dates,
                    'title': {'text': 'Дата'},
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
            ],
            'credits': {
                'enabled': False,
            },
            'exporting': {
                'enabled': False,
            },
        }

        chart_income = {
            'chart': {'type': 'line'},
            'title': {'text': 'Статистика по доходам'},
            'xAxis': [
                {
                    'categories': unique_income_dates,
                    'title': {'text': 'Дата'},
                },
            ],
            'yAxis': {'title': {'text': 'Сумма'}},
            'series': [
                {
                    'name': 'Доходы',
                    'data': unique_income_amounts,
                    'color': 'green',
                    'xAxis': 0,
                },
            ],
            'credits': {
                'enabled': False,
            },
            'exporting': {
                'enabled': False,
            },
        }

        dump_expense = json.dumps(chart_expense)
        dump_income = json.dumps(chart_income)
        category_month = self.expense_category_month(request)
        return render(
            request,
            self.template_name,
            {
                'chart_expense': dump_expense,
                'chart_income': dump_income,
                'category_month': category_month,
            },
        )
