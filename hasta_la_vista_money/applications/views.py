from operator import itemgetter

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, ProtectedError, Sum
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, TemplateView, UpdateView
from hasta_la_vista_money.account.forms import (
    AddAccountForm,
    TransferMoneyAccountForm,
)
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.constants import MessageOnSite
from hasta_la_vista_money.custom_mixin import (
    CustomNoPermissionMixin,
    UpdateViewMixin,
)
from hasta_la_vista_money.expense.models import Expense
from hasta_la_vista_money.income.models import Income
from hasta_la_vista_money.receipts.models import Receipt


class PageApplication(
    CustomNoPermissionMixin,
    SuccessMessageMixin,
    TemplateView,
):
    """Отображает список приложений в проекте на сайте."""

    model = Account
    template_name = 'applications/page_application.html'
    context_object_name = 'applications'
    no_permission_url = reverse_lazy('login')
    success_url = 'applications:list'

    @classmethod
    def collect_info_receipt(cls, user):
        return (
            Receipt.objects.filter(
                user=user,
            )
            .annotate(
                month=TruncMonth('receipt_date'),
            )
            .values(
                'month',
                'account__name_account',
            )
            .annotate(
                count=Count('id'),
                total_amount=Sum('total_sum'),
            )
            .order_by('-month')
        )

    @classmethod
    def collect_info_income_expense(cls, user):
        expenses = (
            Expense.objects.filter(user=user)
            .values(
                'id',
                'date',
                'account__name_account',
                'category__name',
                'amount',
            )
            .order_by('-date')
        )

        income = (
            Income.objects.filter(
                user=user,
            )
            .values(
                'id',
                'date',
                'account__name_account',
                'category__name',
                'amount',
            )
            .order_by('-date')
        )

        return sorted(
            list(expenses) + list(income),
            key=itemgetter('date'),
            reverse=True,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            accounts = Account.objects.filter(
                user=self.request.userб
            ).order_by('name_account')

            receipt_info_by_month = self.collect_info_receipt(
                user=self.request.user,
            )

            income_expense = self.collect_info_income_expense(
                user=self.request.user,
            )

            initial_form_data = {
                'from_account': accounts.first(),
                'to_account': accounts.first(),
            }

            context['accounts'] = accounts
            context['add_account_form'] = AddAccountForm()
            context['transfer_money_form'] = TransferMoneyAccountForm(
                user=self.request.user,
                initial=initial_form_data,
            )
            context['receipt_info_by_month'] = receipt_info_by_month
            context['income_expense'] = income_expense
        return context

    def post(self, request, *args, **kwargs):
        accounts = Account.objects.filter(user=self.request.user).all()
        account_form = AddAccountForm(request.POST)

        receipt_info_by_month = self.collect_info_receipt(
            user=self.request.user,
        )

        income_expense = self.collect_info_income_expense(
            user=self.request.user,
        )

        if account_form.is_valid():
            add_account = account_form.save(commit=False)
            if request.user.is_authenticated:
                add_account.user = request.user
                add_account.save()
                return redirect(reverse_lazy(self.success_url))

        return render(
            request,
            self.template_name,
            {
                'accounts': accounts,
                'income_expense': income_expense,
                'add_account_form': account_form,
                'receipt_info_by_month': receipt_info_by_month,
            },
        )


class ChangeAccountView(
    CustomNoPermissionMixin,
    SuccessMessageMixin,
    UpdateView,
    UpdateViewMixin,
):
    model = Account
    form_class = AddAccountForm
    template_name = 'account/change_account.html'
    success_url = reverse_lazy('applications:list')
    success_message = MessageOnSite.SUCCESS_MESSAGE_CHANGED_ACCOUNT.value

    def get(self, request, *args, **kwargs):
        return self.get_update_form(
            self.form_class,
            'add_account_form',
        )


class TransferMoneyAccountView(
    CustomNoPermissionMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = Account
    template_name = 'applications/page_application.html'
    form_class = TransferMoneyAccountForm
    success_message = MessageOnSite.SUCCESS_MESSAGE_TRANSFER_MONEY.value

    def post(self, request, *args, **kwargs):
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


class DeleteAccountView(DeleteView):
    model = Account
    success_url = reverse_lazy('applications:list')

    def form_valid(self, form):
        try:
            account = self.get_object()
            account.delete()
            messages.success(self.request, 'Счёт успешно удалён!')
            return super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, 'Счёт не может быть удалён!')
            return redirect(self.success_url)
