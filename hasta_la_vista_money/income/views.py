from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django_filters.views import FilterView
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.buttons_delete import (
    button_delete_category,
    button_delete_income,
)
from hasta_la_vista_money.custom_mixin import CustomNoPermissionMixin
from hasta_la_vista_money.income.forms import AddCategoryIncomeForm, IncomeForm
from hasta_la_vista_money.income.models import Income, IncomeType


class IncomeView(CustomNoPermissionMixin, SuccessMessageMixin, FilterView):
    """Представление просмотра доходов из модели, на сайте."""

    model = Income
    template_name = 'income/income.html'
    context_object_name = 'incomes'
    no_permission_url = reverse_lazy('login')
    success_url = 'income:list'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            income_form = IncomeForm()
            add_category_income_form = AddCategoryIncomeForm()

            income_form.fields['account'].queryset = Account.objects.filter(
                user=request.user,
            )
            sort_by_month = Income.objects.filter(
                user=request.user,
            ).order_by('-date')
            categories = IncomeType.objects.filter(user=request.user).all()
            return render(
                request,
                self.template_name,
                {
                    'add_category_income_form': add_category_income_form,
                    'categories': categories,
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
        if 'delete_category_income_button' in request.POST:
            category_id = request.POST.get('category_income_id')
            button_delete_category(
                IncomeType,
                request,
                object_id=category_id,
                url=self.success_url,
            )

        categories = IncomeType.objects.filter(user=request.user).all()
        income_form = IncomeForm(request.POST)
        add_category_income_form = AddCategoryIncomeForm(request.POST)

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

        elif add_category_income_form.is_valid():
            category_form = add_category_income_form.save(commit=False)
            category_form.user = request.user
            category_form.save()
            messages.success(request, 'Категория добавлена!')
            return redirect(self.success_url)
        else:
            return render(
                request,
                self.template_name,
                {'income_form': income_form},
                {'add_category_income_form': add_category_income_form},
                {'categories': categories},
            )
