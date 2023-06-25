from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django_filters.views import FilterView
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.buttons_delete import button_delete_income
from hasta_la_vista_money.custom_mixin import CustomNoPermissionMixin
from hasta_la_vista_money.income.forms import IncomeForm
from hasta_la_vista_money.income.models import Income


class IncomeView(CustomNoPermissionMixin, SuccessMessageMixin, FilterView):
    """Представление просмотра доходов из модели, на сайте."""

    model = Income
    template_name = 'income/income.html'
    context_object_name = 'incomes'
    no_permission_url = reverse_lazy('login')
    success_url = 'income:list'

    def get(self, request, *args, **kwargs):
        if request.user:
            income_form = IncomeForm()
            income_form.fields['account'].queryset = Account.objects.filter(
                user=request.user,
            )
            sort_by_month = Income.objects.filter(
                user=request.user,
            ).order_by('-date')

            return render(
                request,
                self.template_name,
                {
                    'income_by_month': sort_by_month,
                    'income_form': income_form,
                },
            )

    def post(self, request, *args, **kwargs):  # noqa: WPS210
        if 'delete_income_button' in request.POST:
            income_id = request.POST.get('income_id')
            button_delete_income(
                model=Income,
                request=request,
                object_id=income_id,
                url=self.success_url,
            )

        income_form = IncomeForm(request.POST)

        if income_form.is_valid():
            income = income_form.save(commit=False)
            amount = income_form.cleaned_data.get('amount')
            account = income_form.cleaned_data.get('account')
            account_balance = get_object_or_404(Account, id=account.id)

            if account_balance.user == request.user:
                account_balance.balance += amount
                account_balance.save()
                income.user = request.user
                income.save()
                return redirect(reverse_lazy(self.success_url))
        else:
            return render(
                request,
                self.template_name,
                {'income_form': income_form},
            )
