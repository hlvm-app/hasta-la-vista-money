from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, UpdateView
from django.views.generic.edit import DeletionMixin
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.commonlogic.custom_paginator import (
    paginator_custom_view,
)
from hasta_la_vista_money.commonlogic.views import (
    IncomeExpenseCreateViewMixin,
    build_category_tree,
    create_object_view,
    get_queryset_type_income_expenses,
)
from hasta_la_vista_money.constants import (
    MessageOnSite,
    SuccessUrlView,
    TemplateHTMLView,
)
from hasta_la_vista_money.custom_mixin import (
    CustomNoPermissionMixin,
    DeleteCategoryMixin,
    ExpenseIncomeCategoryCreateViewMixin,
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
        depth_limit = 3
        if user:
            categories = (
                user.category_income_users.select_related('user')
                .values(
                    'id',
                    'name',
                    'parent_category',
                    'parent_category__name',
                )
                .order_by('parent_category_id')
                .all()
            )

            flattened_categories = build_category_tree(
                categories,
                depth=depth_limit,
            )
            income_form = IncomeForm(user=self.request.user, depth=depth_limit)
            income_form.fields[
                'account'
            ].queryset = user.account_users.select_related('user').all()

            add_category_income_form = AddCategoryIncomeForm(
                user=self.request.user,
                depth=depth_limit,
            )

            income_by_month = user.income_users.select_related(
                'user',
                'account',
            ).values(
                'id',
                'date',
                'account__name_account',
                'category__name',
                'category__parent_category__name',
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
            context['flattened_categories'] = flattened_categories

            return context


class IncomeCreateView(
    CustomNoPermissionMixin,
    SuccessMessageMixin,
    IncomeExpenseCreateViewMixin,
):
    model = Income
    template_name = TemplateHTMLView.INCOME_TEMPLATE.value
    no_permission_url = reverse_lazy('login')
    form_class = IncomeForm
    success_url = reverse_lazy(SuccessUrlView.INCOME_URL.value)
    depth_limit = 3

    def form_valid(self, form):
        if form.is_valid():
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            response_data = create_object_view(
                form=form,
                model=IncomeCategory,
                request=self.request,
                message=MessageOnSite.SUCCESS_INCOME_ADDED.value,
            )
            return JsonResponse(response_data)


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
    depth_limit = 3

    def get_object(self, queryset=None):
        return get_object_or_404(
            Income,
            pk=self.kwargs['pk'],
            user=self.request.user,
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['depth'] = self.depth_limit
        return kwargs

    def get_context_data(self, **kwargs):
        user = get_object_or_404(User, username=self.request.user)
        context = super().get_context_data(**kwargs)
        form_class = self.get_form_class()
        form = form_class(**self.get_form_kwargs())
        form.fields['account'].queryset = user.account_users.select_related(
            'user',
        ).all()
        context['income_form'] = form
        return context

    def form_valid(self, form):
        income = get_queryset_type_income_expenses(self.object.id, Income, form)

        amount = form.cleaned_data.get('amount')
        account = form.cleaned_data.get('account')
        account_balance = get_object_or_404(Account, id=account.id)
        old_account_balance = get_object_or_404(Account, id=income.account.id)

        if account_balance.user == self.request.user:
            if income:
                old_amount = income.amount
                account_balance.balance -= old_amount

            if income.account != account:
                old_account_balance.balance -= amount
                account_balance.balance += amount

            old_account_balance.save()
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


class IncomeCategoryCreateView(ExpenseIncomeCategoryCreateViewMixin):
    model = IncomeCategory
    template_name = TemplateHTMLView.INCOME_TEMPLATE.value
    success_url = reverse_lazy(SuccessUrlView.INCOME_URL.value)
    form_class = AddCategoryIncomeForm
    depth = 3


class IncomeCategoryDeleteView(DeleteCategoryMixin):
    model = IncomeCategory
    success_url = reverse_lazy(SuccessUrlView.INCOME_URL.value)
