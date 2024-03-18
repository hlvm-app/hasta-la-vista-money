from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, UpdateView
from django_filters.views import FilterView
from hasta_la_vista_money import constants
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
from hasta_la_vista_money.custom_mixin import (
    CustomNoPermissionMixin,
    DeleteObjectMixin,
    ExpenseIncomeCategoryCreateViewMixin,
    UpdateViewMixin,
)
from hasta_la_vista_money.expense.filters import ExpenseFilter
from hasta_la_vista_money.expense.forms import AddCategoryForm, AddExpenseForm
from hasta_la_vista_money.expense.models import Expense, ExpenseCategory
from hasta_la_vista_money.users.models import CustomUser


class BaseView:
    template_name = 'expense/expense.html'
    success_url = reverse_lazy('expense:list')


class ExpenseBaseView(BaseView):
    model = Expense


class ExpenseCategoryBaseView(BaseView):
    model = ExpenseCategory


class ExpenseView(
    CustomNoPermissionMixin,
    ExpenseBaseView,
    SuccessMessageMixin,
    FilterView,
):
    paginate_by = 10
    context_object_name = 'expense'
    filterset_class = ExpenseFilter
    no_permission_url = reverse_lazy('login')

    def get_context_data(self, *args, **kwargs):
        """
        Метод отображения расходов по месяцам на странице.

        :return: Рендеринг данных на странице сайта.
        """
        user = get_object_or_404(CustomUser, username=self.request.user)
        depth_limit = 3
        if user:
            expense_categories = (
                user.category_expense_users.select_related('user')
                .values(
                    'id',
                    'name',
                    'parent_category',
                    'parent_category__name',
                )
                .order_by('name', 'parent_category')
                .all()
            )
            expense_filter = ExpenseFilter(
                self.request.GET,
                queryset=Expense.objects.all(),
                user=self.request.user,
            )
            flattened_categories = build_category_tree(
                expense_categories,
                depth=depth_limit,
            )
            categories = (
                user.category_expense_users.select_related('user')
                .order_by('parent_category__name', 'name')
                .all()
            )
            add_expense_form = AddExpenseForm(
                user=self.request.user,
                depth=depth_limit,
                category_queryset=categories,
            )
            add_expense_form.fields[
                'account'
            ].queryset = user.account_users.select_related('user').all()

            add_category_form = AddCategoryForm(
                user=self.request.user,
                depth=depth_limit,
            )

            expenses = expense_filter.qs

            # Paginator expense table
            pages_expense = paginator_custom_view(
                self.request,
                expenses,
                self.paginate_by,
                'expenses',
            )

            context = super().get_context_data(**kwargs)
            context['add_category_form'] = add_category_form
            context['expense_filter'] = expense_filter
            context['categories'] = expense_categories
            context['expenses'] = pages_expense
            context['add_expense_form'] = add_expense_form
            context['flattened_categories'] = flattened_categories

            return context


class ExpenseCreateView(
    CustomNoPermissionMixin,
    SuccessMessageMixin,
    ExpenseBaseView,
    IncomeExpenseCreateViewMixin,
):
    no_permission_url = reverse_lazy('login')
    form_class = AddExpenseForm
    depth_limit = 3

    def form_valid(self, form):
        if form.is_valid():
            response_data = create_object_view(
                form=form,
                model=ExpenseCategory,
                request=self.request,
                message=constants.SUCCESS_EXPENSE_ADDED,
            )
            return JsonResponse(response_data)


class ExpenseUpdateView(
    CustomNoPermissionMixin,
    SuccessMessageMixin,
    ExpenseBaseView,
    UpdateView,
    UpdateViewMixin,
):
    template_name = 'expense/change_expense.html'
    form_class = AddExpenseForm
    no_permission_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return get_object_or_404(
            Expense,
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
        context['add_expense_form'] = form
        return context

    def form_valid(self, form):
        expense = get_queryset_type_income_expenses(
            self.object.id,
            Expense,
            form,
        )

        amount = form.cleaned_data.get('amount')
        account = form.cleaned_data.get('account')
        account_balance = get_object_or_404(Account, id=account.id)
        old_account_balance = get_object_or_404(Account, id=expense.account.id)

        if account_balance.user == self.request.user:
            if expense:
                old_amount = expense.amount
                account_balance.balance += old_amount

            if expense.account != account:
                old_account_balance.balance += amount
                account_balance.balance -= amount

            old_account_balance.save()
            account_balance.balance -= amount
            account_balance.save()

            expense.user = self.request.user
            expense.amount = amount
            expense.save()

            messages.success(
                self.request,
                constants.SUCCESS_EXPENSE_UPDATE,
            )
            return super().form_valid(form)


class ExpenseDeleteView(ExpenseBaseView, DetailView, DeleteView):
    context_object_name = 'expense'
    no_permission_url = reverse_lazy('login')

    def form_valid(self, form):
        expense = self.get_object()
        account = expense.account
        amount = expense.amount
        account_balance = get_object_or_404(Account, id=account.id)

        if account_balance.user == self.request.user:
            account_balance.balance += amount
            account_balance.save()
            messages.success(
                self.request,
                constants.SUCCESS_EXPENSE_DELETED,
            )
            return super().form_valid(form)


class ExpenseCategoryCreateView(
    ExpenseCategoryBaseView,
    ExpenseIncomeCategoryCreateViewMixin,
):
    form_class = AddCategoryForm
    depth = 3


class ExpenseCategoryDeleteView(
    ExpenseCategoryBaseView,
    DeleteObjectMixin,
):
    success_message = constants.SUCCESS_CATEGORY_EXPENSE_DELETED
    error_message = constants.ACCESS_DENIED_DELETE_EXPENSE_CATEGORY
