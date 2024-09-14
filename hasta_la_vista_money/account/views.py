import json

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from hasta_la_vista_money import constants
from hasta_la_vista_money.account.forms import (
    AddAccountForm,
    TransferMoneyAccountForm,
)
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.account.prepare import (
    collect_info_expense,
    collect_info_income,
    sort_expense_income,
)
from hasta_la_vista_money.commonlogic.views import collect_info_receipt
from hasta_la_vista_money.custom_mixin import (
    CustomNoPermissionMixin,
    DeleteObjectMixin,
)
from hasta_la_vista_money.expense.models import Expense
from hasta_la_vista_money.income.models import Income
from hasta_la_vista_money.users.models import User


class BaseView:
    template_name = 'account/account.html'
    success_url = reverse_lazy('account:list')


class AccountBaseView(BaseView):
    model = Account


class AccountView(
    CustomNoPermissionMixin,
    SuccessMessageMixin,
    AccountBaseView,
    ListView,
):
    """Отображает список приложений в проекте на сайте."""

    context_object_name = 'account'
    no_permission_url = reverse_lazy('login')

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

    def get_context_data(self, **kwargs) -> dict:
        expense_dataset, income_dataset = self.collect_datasets(self.request)

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

        # Combine unique dates for both expense and income to create a single time axis
        all_dates = sorted(set(unique_expense_dates + unique_income_dates))

        # Create data points for expense and income that match the combined dates
        expense_series_data = [
            unique_expense_amounts[unique_expense_dates.index(date)]
            if date in unique_expense_dates
            else 0
            for date in all_dates
        ]

        income_series_data = [
            unique_income_amounts[unique_income_dates.index(date)]
            if date in unique_income_dates
            else 0
            for date in all_dates
        ]

        # Create a combined chart with both expense and income data
        chart_combined = {
            'chart': {
                'type': 'line',
                'borderColor': '#000000',
                'borderWidth': 1,
                'height': 300,
            },
            'title': {'text': 'Аналитика'},
            'xAxis': [
                {
                    'categories': all_dates,
                    'title': {'text': 'Дата'},
                },
            ],
            'yAxis': {'title': {'text': 'Сумма'}},
            'series': [
                {
                    'name': 'Расходы',
                    'data': expense_series_data,
                    'color': 'red',
                },
                {
                    'name': 'Доходы',
                    'data': income_series_data,
                    'color': 'green',
                },
            ],
            'credits': {
                'enabled': False,
            },
            'exporting': {
                'enabled': False,
            },
            'responsive': {
                'rules': [
                    {
                        'condition': {'maxWidth': 700},
                        'chartOptions': {
                            'legend': {
                                'layout': 'horizontal',
                                'align': 'center',
                                'verticalAlign': 'bottom',
                            },
                        },
                    },
                ],
            },
        }

        if self.request.user.is_authenticated:
            user = get_object_or_404(
                User,
                username=self.request.user,
            )

            accounts = user.account_users.select_related('user').all()

            receipt_info_by_month = collect_info_receipt(user=user)

            income = collect_info_income(user)
            expenses = collect_info_expense(user)
            income_expense = sort_expense_income(expenses, income)

            account_transfer_money = user.account_users.select_related(
                'user',
            ).all()
            initial_form_data = {
                'from_account': account_transfer_money.first(),
                'to_account': account_transfer_money.first(),
            }

            transfer_money_log = user.transfer_money.select_related(
                'to_account',
                'from_account',
            ).all()

            context = super().get_context_data(**kwargs)
            context['accounts'] = accounts
            context['add_account_form'] = AddAccountForm()
            context['transfer_money_form'] = TransferMoneyAccountForm(
                user=self.request.user,
                initial=initial_form_data,
            )
            context['receipt_info_by_month'] = receipt_info_by_month
            context['income_expense'] = income_expense
            context['transfer_money_log'] = transfer_money_log
            context['chart_combine'] = json.dumps(chart_combined)

            return context


class AccountCreateView(SuccessMessageMixin, AccountBaseView, CreateView):
    form_class = AddAccountForm
    no_permission_url = reverse_lazy('login')

    def post(self, request: WSGIRequest, *args, **kwargs) -> JsonResponse:
        account_form = AddAccountForm(request.POST)
        if account_form.is_valid():
            add_account = account_form.save(commit=False)
            add_account.user = request.user
            add_account.save()
            messages.success(
                request,
                constants.SUCCESS_MESSAGE_ADDED_ACCOUNT,
            )
            response_data = {'success': True}
        else:
            response_data = {
                'success': False,
                'errors': account_form.errors,
            }
        return JsonResponse(response_data)


class ChangeAccountView(
    CustomNoPermissionMixin,
    SuccessMessageMixin,
    AccountBaseView,
    UpdateView,
):
    form_class = AddAccountForm
    template_name = 'account/change_account.html'
    success_message = constants.SUCCESS_MESSAGE_CHANGED_ACCOUNT

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_class = self.get_form_class()
        form = form_class(**self.get_form_kwargs())
        context['add_account_form'] = form
        return context


class TransferMoneyAccountView(
    CustomNoPermissionMixin,
    SuccessMessageMixin,
    AccountBaseView,
    UpdateView,
):
    form_class = TransferMoneyAccountForm
    success_message = constants.SUCCESS_MESSAGE_TRANSFER_MONEY

    def post(self, request: WSGIRequest, *args, **kwargs) -> JsonResponse:
        transfer_money_form = TransferMoneyAccountForm(
            user=request.user,
            data=request.POST,
        )

        valid_form = (
            transfer_money_form.is_valid()
            and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        )
        if valid_form:
            transfer_log = transfer_money_form.save(commit=False)

            if transfer_log is not None:
                transfer_log.user = request.user
                transfer_log.save()
                messages.success(request, self.success_message)
            response_data = {'success': True}
        else:
            response_data = {
                'success': False,
                'errors': transfer_money_form.errors,
            }
        return JsonResponse(response_data)


class DeleteAccountView(AccountBaseView, DeleteObjectMixin):
    success_message = constants.SUCCESS_MESSAGE_DELETE_ACCOUNT[:]
    error_message = constants.UNSUCCESSFULLY_MESSAGE_DELETE_ACCOUNT[:]
