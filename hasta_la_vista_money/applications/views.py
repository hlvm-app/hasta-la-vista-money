from operator import itemgetter

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import ProtectedError
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    TemplateView,
    UpdateView,
)
from hasta_la_vista_money.account.forms import (
    AddAccountForm,
    TransferMoneyAccountForm,
)
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.commonlogic.views import collect_info_receipt
from hasta_la_vista_money.constants import MessageOnSite
from hasta_la_vista_money.custom_mixin import (
    CustomNoPermissionMixin,
    UpdateViewMixin,
)
from hasta_la_vista_money.income.models import Income
from hasta_la_vista_money.users.models import User


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

    @classmethod
    def collect_info_income_expense(cls, user: User) -> list:
        expenses = user.expense_users.select_related('user').values(
            'id',
            'date',
            'account__name_account',
            'category__name',
            'amount',
        )

        income = user.income_users.select_related('user').values(
            'id',
            'date',
            'account__name_account',
            'category__name',
            'amount',
        )

        return sorted(
            list(expenses) + list(income),
            key=itemgetter('date'),
            reverse=True,
        )

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        self.request: WSGIRequest = self.request

        if self.request.user.is_authenticated:
            user = get_object_or_404(
                User,
                username=self.request.user,
            )

            accounts = user.account_users.select_related('user').all()

            receipt_info_by_month = collect_info_receipt(user=user)

            income_expense = self.collect_info_income_expense(
                user=user,
            )

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


class AccountCreateView(SuccessMessageMixin, CreateView):
    model = Account
    template_name = 'applications/page_application.html'
    form_class = AddAccountForm
    no_permission_url = reverse_lazy('login')
    success_url = reverse_lazy('applications:list')

    def post(self, request: WSGIRequest, *args, **kwargs) -> JsonResponse:
        account_form = AddAccountForm(request.POST)
        if account_form.is_valid():
            add_account = account_form.save(commit=False)
            add_account.user = request.user
            add_account.save()
            messages.success(
                request,
                MessageOnSite.SUCCESS_MESSAGE_ADDED_ACCOUNT.value,
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
    UpdateView,
    UpdateViewMixin,
):
    model = Account
    form_class = AddAccountForm
    template_name = 'account/change_account.html'
    success_url = reverse_lazy('applications:list')
    success_message = MessageOnSite.SUCCESS_MESSAGE_CHANGED_ACCOUNT.value

    def get(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        user = Income.objects.filter(user=request.user).first()
        if user:
            return self.get_update_form(
                self.form_class,
                'add_account_form',
            )
        raise Http404


class TransferMoneyAccountView(
    CustomNoPermissionMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = Account
    template_name = 'applications/page_application.html'
    form_class = TransferMoneyAccountForm
    success_message = MessageOnSite.SUCCESS_MESSAGE_TRANSFER_MONEY.value

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
