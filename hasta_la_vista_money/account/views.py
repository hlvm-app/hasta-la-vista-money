from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.handlers.wsgi import WSGIRequest
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
from hasta_la_vista_money.account.serializers import AccountSerializer
from hasta_la_vista_money.commonlogic.views import collect_info_receipt
from hasta_la_vista_money.custom_mixin import (
    CustomNoPermissionMixin,
    DeleteObjectMixin,
)
from hasta_la_vista_money.users.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


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


class AccountListCreateAPIView(ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticated,)

    @property
    def queryset(self):
        return Account.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = AccountSerializer(queryset, many=True)
        return Response(serializer.data)


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
