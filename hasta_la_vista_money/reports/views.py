from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import CharField, IntegerField, Sum, Value
from django.db.models.functions import Cast, Concat
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
from hasta_la_vista_money.income.models import Income
from hasta_la_vista_money.receipts.models import Receipt


class ReportView(CustomNoPermissionMixin, SuccessMessageMixin, TemplateView):
    template_name = 'reports/reports.html'
    no_permission_url = reverse_lazy('login')

    @classmethod
    def get_month_total_amount_income(cls):
        return Income.objects.values('month').annotate(
            total_amount=Sum('amount'),
        )

    @classmethod
    def get_month_sum_receipt(cls):
        return Receipt.objects.annotate(
            month_year=Concat(
                Cast('receipt_date__month', CharField()),
                Value(' '),
                'receipt_date__year',
                output_field=CharField(),
            ),
        ).values('month_year').annotate(total_sum=Sum('total_sum')).order_by(
            Cast('receipt_date__month', IntegerField()),
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
        receipt_data = [
            {
                'month_year': MONTH_NAMES.get(
                    int(receipt_list_month_total_sum['month_year'].split()[0]),
                    'Неизвестно',
                ) + ' ' + receipt_list_month_total_sum[
                    'month_year'
                ].split()[1],
                'total_sum': receipt_list_month_total_sum[
                    'total_sum'
                ],
            }
            for receipt_list_month_total_sum in self.get_month_sum_receipt()
        ]

        # Создание словаря для хранения сумм доходов/чеков по месяцам
        income_amounts = {
            income_dict_date_sums[
                'month'
            ]: income_dict_date_sums[
                'total_amount'
            ] for income_dict_date_sums in self.get_month_total_amount_income()
        }

        receipt_sums = {
            receipt_dict_date_sums[
                'month_year'
            ]: receipt_dict_date_sums[
                'total_sum'
            ] for receipt_dict_date_sums in receipt_data
        }

        # Создание списков сумм доходов/чеков в правильном порядке
        income_amounts = [
            float(income_amounts.get(
                month_year, 0,
            ),
            ) for month_year in self.get_list_months_year()
        ]

        receipt_sums = [
            float(
                receipt_sums.get(month_year, 0),
            ) for month_year in self.get_list_months_year()
        ]

        return render(request, self.template_name, {
            'income_amounts': income_amounts,
            'receipt_sums': receipt_sums,
        })
