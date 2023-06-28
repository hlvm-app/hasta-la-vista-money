from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError, Count, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, TemplateView
from hasta_la_vista_money.account.forms import AddAccountForm
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.custom_mixin import CustomNoPermissionMixin
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            accounts = Account.objects.filter(user=self.request.user)
            receipt_info_by_month = Receipt.objects.filter(
                user=self.request.user,
            ).annotate(
                month=TruncMonth('receipt_date'),
            ).values(
                'month',
                'account__name_account',
            ).annotate(
                count=Count('id'),
                total_amount=Sum('total_sum'),
            ).order_by('-month')

            expenses = Expense.objects.filter(user=self.request.user).values(
                'id',
                'date',
                'account__name_account',
                'category__name',
                'amount',
            ).order_by('-date')

            income_by_month = Income.objects.filter(
                user=self.request.user,
            ).order_by('-date')

            context['accounts'] = accounts
            context['add_account_form'] = AddAccountForm()
            context['receipt_info_by_month'] = receipt_info_by_month
            context['expenses'] = expenses
            context['income_by_month'] = income_by_month
        return context

    def post(self, request, *args, **kwargs):
        accounts = Account.objects.filter(user=self.request.user).all()
        account_form = AddAccountForm(request.POST)
        if account_form.is_valid():
            add_account = account_form.save(commit=False)
            if request.user.is_authenticated:
                add_account.user = request.user
                add_account.save()
                return redirect(reverse_lazy(self.success_url))
        else:
            return render(
                request,
                self.template_name,
                {
                    'accounts': accounts,
                    'add_account_form': account_form,
                },
            )


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
