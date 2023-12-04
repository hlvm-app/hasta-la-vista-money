from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, UpdateView
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.commonlogic.custom_paginator import (
    paginator_custom_view,
)
from hasta_la_vista_money.commonlogic.views import (
    IncomeExpenseCreateViewMixin,
    build_category_tree,
    create_object_view,
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
from hasta_la_vista_money.expense.forms import AddCategoryForm, AddExpenseForm
from hasta_la_vista_money.expense.models import Expense, ExpenseCategory
from hasta_la_vista_money.users.models import User


class ExpenseView(CustomNoPermissionMixin, SuccessMessageMixin, ListView):
    paginate_by = 10
    model = Expense
    template_name = TemplateHTMLView.EXPENSE_TEMPLATE.value
    context_object_name = 'expense'
    no_permission_url = reverse_lazy('login')
    success_url = SuccessUrlView.EXPENSE_URL.value

    def get_context_data(self, *args, **kwargs):
        """
        Метод отображения расходов по месяцам на странице.

        :return: Рендеринг данных на странице сайта.
        """
        user = get_object_or_404(User, username=self.request.user)
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
            flattened_categories = build_category_tree(
                expense_categories,
                depth=depth_limit,
            )
            add_expense_form = AddExpenseForm(
                user=self.request.user,
                depth=depth_limit,
            )
            add_expense_form.fields[
                'account'
            ].queryset = user.account_users.select_related('user').all()

            add_category_form = AddCategoryForm(
                user=self.request.user,
                depth=depth_limit,
            )

            expenses = user.expense_users.select_related(
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

            # Paginator expense table
            pages_expense = paginator_custom_view(
                self.request,
                expenses,
                self.paginate_by,
                'expenses',
            )

            context = super().get_context_data(**kwargs)
            context['add_category_form'] = add_category_form
            context['categories'] = expense_categories
            context['expenses'] = pages_expense
            context['add_expense_form'] = add_expense_form
            context['flattened_categories'] = flattened_categories

            return context


class ExpenseCreateView(
    CustomNoPermissionMixin,
    SuccessMessageMixin,
    IncomeExpenseCreateViewMixin,
):
    model = Expense
    template_name = TemplateHTMLView.EXPENSE_TEMPLATE.value
    no_permission_url = reverse_lazy('login')
    form_class = AddExpenseForm
    success_url = reverse_lazy(SuccessUrlView.EXPENSE_URL.value)
    depth_limit = 3

    def form_valid(self, form):
        if form.is_valid():
            response_data = create_object_view(
                form=form,
                model=ExpenseCategory,
                request=self.request,
                message=MessageOnSite.SUCCESS_EXPENSE_ADDED.value,
            )
            return JsonResponse(response_data)


class ExpenseUpdateView(
    CustomNoPermissionMixin,
    SuccessMessageMixin,
    UpdateView,
    UpdateViewMixin,
):
    model = Expense
    template_name = 'expense/change_expense.html'
    form_class = AddExpenseForm
    no_permission_url = reverse_lazy('login')
    success_url = reverse_lazy(SuccessUrlView.EXPENSE_URL.value)

    def get_object(self, queryset=None):  # noqa: WPS615
        return get_object_or_404(Expense, pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['depth'] = self.depth_limit
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_class = self.get_form_class()
        form = form_class(**self.get_form_kwargs())
        context['add_expense_form'] = form
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        expense_id = self.get_object().id
        if expense_id:
            expense = get_object_or_404(Expense, id=expense_id)
        else:
            expense = form.save(commit=False)

        amount = form.cleaned_data.get('amount')
        account = form.cleaned_data.get('account')
        account_balance = get_object_or_404(Account, id=account.id)

        if account_balance.user == self.request.user:
            if expense_id:
                old_amount = expense.amount
                account_balance.balance += old_amount
            account_balance.balance -= amount
            account_balance.save()

            expense.user = self.request.user
            expense.amount = amount
            expense.save()

            messages.success(
                self.request,
                MessageOnSite.SUCCESS_EXPENSE_UPDATE.value,
            )
            return super().form_valid(form)


class ExpenseDeleteView(DetailView, DeleteView):
    model = Expense
    template_name = TemplateHTMLView.EXPENSE_TEMPLATE.value
    context_object_name = 'expense'
    no_permission_url = reverse_lazy('login')
    success_url = reverse_lazy(SuccessUrlView.EXPENSE_URL.value)

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
                MessageOnSite.SUCCESS_EXPENSE_DELETED.value,
            )
            return super().form_valid(form)


class ExpenseCategoryCreateView(ExpenseIncomeCategoryCreateViewMixin):
    model: type[ExpenseCategory] = ExpenseCategory
    template_name = TemplateHTMLView.EXPENSE_TEMPLATE.value
    success_url = reverse_lazy(SuccessUrlView.EXPENSE_URL.value)
    form_class = AddCategoryForm
    depth = 3

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['depth'] = self.depth
        return kwargs


class ExpenseCategoryDeleteView(DeleteCategoryMixin):
    model: type[ExpenseCategory] = ExpenseCategory
    success_url = reverse_lazy(SuccessUrlView.EXPENSE_URL.value)
