from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, UpdateView
from django.views.generic.edit import CreateView, DeletionMixin
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.commonlogic.custom_paginator import (
    paginator_custom_view,
)
from hasta_la_vista_money.commonlogic.views import create_object_view
from hasta_la_vista_money.constants import (
    MessageOnSite,
    SuccessUrlView,
    TemplateHTMLView,
)
from hasta_la_vista_money.custom_mixin import (
    CustomNoPermissionMixin,
    DeleteCategoryMixin,
    ExpenseIncomeFormValidCreateMixin,
    UpdateViewMixin,
)
from hasta_la_vista_money.income.forms import AddCategoryIncomeForm, IncomeForm
from hasta_la_vista_money.income.models import Income, IncomeCategory
from hasta_la_vista_money.users.models import User


class IncomeView(CustomNoPermissionMixin, SuccessMessageMixin, ListView):
    """Представление просмотра доходов из модели, на сайте."""

    paginate_by = 10
    model = Income
    template_name = TemplateHTMLView.INCOME_TEMPLATE.value
    context_object_name = 'incomes'
    no_permission_url = reverse_lazy('login')
    success_url = SuccessUrlView.INCOME_URL.value

    def get_context_data(self, *args, **kwargs):
        user = get_object_or_404(User, username=self.request.user)
        if user:
            income_form = IncomeForm()
            categories = user.category_income_users.select_related('user').all()

            income_form.fields['category'].queryset = categories
            income_form.fields[
                'account'
            ].queryset = user.account_users.select_related('user').all()
            add_category_income_form = AddCategoryIncomeForm()

            income_by_month = user.income_users.select_related(
                'user, account',
            ).values(
                'id',
                'date',
                'account__name_account',
                'category__name',
                'amount',
            )

            pages_income = paginator_custom_view(
                self.request,
                income_by_month,
                self.paginate_by,
                'income',
            )

            context = super().get_context_data(**kwargs)
            context['add_category_income_form'] = add_category_income_form
            context['categories'] = categories
            context['income_by_month'] = pages_income
            context['income_form'] = income_form

            return context


class IncomeCreateView(
    CustomNoPermissionMixin,
    SuccessMessageMixin,
    CreateView,
):
    model = Income
    template_name = TemplateHTMLView.INCOME_TEMPLATE.value
    no_permission_url = reverse_lazy('login')
    form_class = IncomeForm
    success_url = reverse_lazy(SuccessUrlView.INCOME_URL.value)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper.form_action = reverse_lazy('income:create')
        return form

    def post(self, request, *args, **kwargs):
        income_form = IncomeForm(request.POST)
        return create_object_view(
            form=income_form,
            request=request,
            message=MessageOnSite.SUCCESS_INCOME_ADDED.value,
        )


class IncomeUpdateView(
    CustomNoPermissionMixin,
    SuccessMessageMixin,
    UpdateView,
    UpdateViewMixin,
):
    model = Income
    template_name = 'income/change_income.html'
    form_class = IncomeForm
    no_permission_url = reverse_lazy('login')
    success_url = reverse_lazy(SuccessUrlView.INCOME_URL.value)

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.user)
        if user:
            return self.get_update_form(self.form_class, 'income_form')
        raise Http404

    def form_valid(self, form):
        income_id = self.get_object().id
        if income_id:
            income = get_object_or_404(Income, id=income_id)
        else:
            income = form.save(commit=False)

        amount = form.cleaned_data.get('amount')
        account = form.cleaned_data.get('account')
        account_balance = get_object_or_404(Account, id=account.id)

        if account_balance.user == self.request.user:
            if income_id:
                old_amount = income.amount
                account_balance.balance -= old_amount
            account_balance.balance += amount
            account_balance.save()

            income.user = self.request.user
            income.amount = amount
            income.save()
            messages.success(
                self.request,
                MessageOnSite.SUCCESS_INCOME_UPDATE.value,
            )
            return super().form_valid(form)


class IncomeDeleteView(DeleteView, DeletionMixin):
    model = Income
    template_name = TemplateHTMLView.INCOME_TEMPLATE.value
    context_object_name = 'incomes'
    no_permission_url = reverse_lazy('login')
    success_url = reverse_lazy(SuccessUrlView.INCOME_URL.value)

    def form_valid(self, form):
        income = self.get_object()
        account = income.account
        amount = income.amount
        account_balance = get_object_or_404(Account, id=account.id)

        if account_balance.user == self.request.user:
            account_balance.balance -= amount
            account_balance.save()
            messages.success(
                self.request,
                MessageOnSite.SUCCESS_INCOME_DELETED.value,
            )
            return super().form_valid(form)


class IncomeCategoryCreateView(ExpenseIncomeFormValidCreateMixin):
    model = IncomeCategory
    template_name = TemplateHTMLView.INCOME_TEMPLATE.value
    success_url = reverse_lazy(SuccessUrlView.INCOME_URL.value)
    form_class = AddCategoryIncomeForm


class IncomeCategoryDeleteView(DeleteCategoryMixin):
    model = IncomeCategory
    success_url = reverse_lazy(SuccessUrlView.INCOME_URL.value)
