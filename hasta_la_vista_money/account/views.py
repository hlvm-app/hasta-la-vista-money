from operator import itemgetter

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from hasta_la_vista_money import constants
from hasta_la_vista_money.account.forms import (
    AddAccountForm,
    TransferMoneyAccountForm,
)
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.commonlogic.views import collect_info_receipt
from hasta_la_vista_money.custom_mixin import CustomNoPermissionMixin
from hasta_la_vista_money.users.models import User


def collect_info_income(user: User):
    """
    Сбор информации о доходах из базы данных, фильтруемая по пользователю.

    :param user: User
    :return: Queryset
    """
    return user.income_users.select_related('user').values(
        'id',
        'date',
        'account__name_account',
        'category__name',
        'amount',
    )


def collect_info_expense(user: User):
    """
    Сбор информации о расходах из базы данных, фильтруемая по пользователю.

    :param user: User
    :return: Queryset
    """
    return user.expense_users.select_related('user').values(
        'id',
        'date',
        'account__name_account',
        'category__name',
        'amount',
    )


def sort_expense_income(expenses, income):
    """
    Создание отсортированного списка с расходам и доходами.

    :param expenses: Queryset
    :param income: Queryset
    :return: list
    """
    return sorted(
        list(expenses) + list(income),
        key=itemgetter('date'),
        reverse=True,
    )


class BaseView:
    template_name = 'account/account.html'
    success_url = reverse_lazy('applications:list')


class AccountBaseView(BaseView):
    model = Account


class AccountView(
    CustomNoPermissionMixin,
    SuccessMessageMixin,
    AccountBaseView,
    ListView,
):
    """Отображает список приложений в проекте на сайте."""

    context_object_name = 'applications'
    no_permission_url = reverse_lazy('login')

    def get_context_data(self, **kwargs) -> dict:
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
    success_message = _(constants.SUCCESS_MESSAGE_CHANGED_ACCOUNT)

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
    success_message = _(constants.SUCCESS_MESSAGE_TRANSFER_MONEY)

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


class DeleteAccountView(AccountBaseView, DeleteView):
    def form_valid(self, form):
        try:
            account = self.get_object()
            account.delete()
            messages.success(
                self.request,
                constants.SUCCESS_MESSAGE_DELETE_ACCOUNT,
            )
            return super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                constants.UNSUCCESSFULLY_MESSAGE_DELETE_ACCOUNT,
            )
            return redirect(self.success_url)
