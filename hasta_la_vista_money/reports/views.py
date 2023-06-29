import json

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

    def get(self, request, *args, **kwargs):
        dataset = Expense.objects.filter(user=request.user).values(
            'date').annotate(total_amount=Sum('amount')).order_by('date')

        income_dataset = Income.objects.filter(user=request.user).values(
            'date').annotate(total_amount=Sum('amount')).order_by('date')
        print(income_dataset)
        dates = []
        amounts = []
        income_dates = []
        income_amounts = []

        for data in dataset:
            dates.append(data['date'].strftime('%Y-%m-%d'))
            amounts.append(float(data['total_amount']))

        for data in income_dataset:
            income_dates.append(data['date'].strftime('%Y-%m-%d'))
            income_amounts.append(float(data['total_amount']))

        unique_dates = []
        unique_amounts = []


        # Объединение сумм по уникальным датам
        for i, date in enumerate(dates):
            if date not in unique_dates:
                unique_dates.append(date)
                unique_amounts.append(amounts[i])
            else:
                index = unique_dates.index(date)
                unique_amounts[index] += amounts[i]

        unique_income_dates = []
        unique_income_amounts = []
        print(unique_income_amounts)
        print(income_amounts)

        for i, date in enumerate(income_dates):
            if date not in unique_income_dates:
                unique_income_dates.append(date)
                unique_income_amounts.append(income_amounts[i])
            else:
                index = unique_income_dates.index(date)
                unique_income_amounts[index] += income_amounts[i]

        chart = {
            'chart': {'type': 'line'},
            'title': {'text': 'Статистика по расходам и доходам'},
            'xAxis': [
                {'categories': unique_dates,
                 'title': {'text': 'Дата (расходы)'}},
                {'categories': unique_income_dates,
                 'title': {'text': 'Дата (доходы)'}}
            ],
            'yAxis': {'title': {'text': 'Сумма'}},
            'series': [
                {
                    'name': 'Расходы',
                    'data': unique_amounts,
                    'color': 'red',
                    'xAxis': 0
                    # Указываем, что данные для этой серии относятся к первой оси X
                },
                {
                    'name': 'Доходы',
                    'data': unique_income_amounts,
                    'color': 'green',
                    'xAxis': 1
                    # Указываем, что данные для этой серии относятся ко второй оси X
                }
            ],
            'credits': {
                'enabled': False
            },
            'exporting': {
                'enabled': False
            },
        }

        dump = json.dumps(chart)

        return render(request, self.template_name, {'chart': dump})
