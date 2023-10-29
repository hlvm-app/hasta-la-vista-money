from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.commonlogic.custom_paginator import (
    paginator_custom_view,
)
from hasta_la_vista_money.commonlogic.views import (
    collect_info_receipt,
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
    ExpenseIncomeFormValidCreateMixin,
    UpdateViewMixin,
)
from hasta_la_vista_money.expense.forms import AddCategoryForm, AddExpenseForm
from hasta_la_vista_money.expense.models import Expense, ExpenseType


class ExpenseView(CustomNoPermissionMixin, SuccessMessageMixin, ListView):
    paginate_by = 10
    model = Expense
    template_name = TemplateHTMLView.EXPENSE_TEMPLATE.value
    context_object_name = 'expense'
    no_permission_url = reverse_lazy('login')
    success_url = SuccessUrlView.EXPENSE_URL.value

    def get(self, request, *args, **kwargs):
        """
        Метод отображения расходов по месяцам на странице.

        :param request: Запрос данных со страницы сайта.
        :return: Рендеринг данных на странице сайта.
        """
        add_expense_form = AddExpenseForm()
        add_expense_form.fields['account'].queryset = Account.objects.filter(
            user=request.user,
        )
        add_expense_form.fields[
            'category'
        ].queryset = ExpenseType.objects.filter(
            user=request.user,
        )
        add_category_form = AddCategoryForm()

        receipt_info_by_month = collect_info_receipt(user=request.user)

        expenses = Expense.objects.filter(user=request.user).values(
            'id',
            'date',
            'account__name_account',
            'category__name',
            'amount',
        )

        # Paginator expense table
        pages_expense = paginator_custom_view(
            request,
            expenses,
            self.paginate_by,
            'expenses',
        )

        # Paginator receipts table
        pages_receipt_table = paginator_custom_view(
            request,
            receipt_info_by_month,
            self.paginate_by,
            'receipts',
        )

        expense_categories = ExpenseType.objects.filter(user=request.user)

        return render(
            request,
            self.template_name,
            {
                'add_category_form': add_category_form,
                'categories': expense_categories,
                'receipt_info_by_month': pages_receipt_table,
                'expenses': pages_expense,
                'add_expense_form': add_expense_form,
            },
        )

    def post(self, request, *args, **kwargs):
        categories = ExpenseType.objects.filter(user=request.user).all()

        add_category_form = AddCategoryForm(request.POST)

        if add_category_form.is_valid():
            category_form = add_category_form.save(commit=False)
            category_form.user = request.user
            category_form.save()
            messages.success(
                request,
                MessageOnSite.SUCCESS_CATEGORY_ADDED.value,
            )
            return redirect(self.success_url)
        return render(
            request,
            self.template_name,
            {
                'add_category_form': add_category_form,
                'categories': categories,
            },
        )


class ExpenseCreateView(
    CustomNoPermissionMixin,
    SuccessMessageMixin,
    CreateView,
):
    model = Expense
    template_name = TemplateHTMLView.EXPENSE_TEMPLATE.value
    no_permission_url = reverse_lazy('login')
    form_class = AddExpenseForm
    success_url = reverse_lazy(SuccessUrlView.EXPENSE_URL.value)

    def post(self, request, *args, **kwargs):
        add_expense_form = AddExpenseForm(request.POST)
        return create_object_view(
            form=add_expense_form,
            request=request,
            message=MessageOnSite.SUCCESS_EXPENSE_ADDED.value,
        )


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

    def get(self, request, *args, **kwargs):
        user = Expense.objects.filter(user=request.user).first()
        if user:
            return self.get_update_form(
                self.form_class,
                'add_expense_form',
            )
        raise Http404

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


class ExpenseCategoryCreateView(ExpenseIncomeFormValidCreateMixin):
    model = ExpenseType
    template_name = TemplateHTMLView.EXPENSE_TEMPLATE.value
    success_url = reverse_lazy(SuccessUrlView.EXPENSE_URL.value)
    form_class = AddCategoryForm


class ExpenseCategoryDeleteView(DeleteCategoryMixin):
    model: type[ExpenseType] = ExpenseType
    success_url = reverse_lazy(SuccessUrlView.EXPENSE_URL.value)
