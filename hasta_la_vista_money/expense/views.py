from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, ProtectedError, Sum
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
    UpdateView,
)
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.constants import SuccessUrlView, TemplateHTMLView
from hasta_la_vista_money.custom_mixin import (
    CustomNoPermissionMixin,
    DeleteCategoryMixin,
)
from hasta_la_vista_money.expense.forms import AddCategoryForm, AddExpenseForm
from hasta_la_vista_money.expense.models import Expense, ExpenseType
from hasta_la_vista_money.receipts.models import Receipt


class ExpenseView(CustomNoPermissionMixin, SuccessMessageMixin, TemplateView):
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
        if request.user.is_authenticated:
            add_expense_form = AddExpenseForm()
            add_category_form = AddCategoryForm()

            add_expense_form.fields[
                'account'
            ].queryset = Account.objects.filter(
                user=request.user,
            )
            receipt_info_by_month = Receipt.objects.filter(
                user=request.user,
            ).annotate(
                month=TruncMonth('receipt_date'),
            ).values(
                'month',
                'account__name_account',
            ).annotate(
                count=Count('id'),
                total_amount=Sum('total_sum'),
            ).order_by('-month')

            expenses = Expense.objects.filter(user=request.user).values(
                'id',
                'date',
                'account__name_account',
                'category__name',
                'amount',
            ).order_by('-date')

            categories = ExpenseType.objects.filter(user=request.user).all()

            return render(
                request,
                self.template_name,
                {
                    'add_category_form': add_category_form,
                    'categories': categories,
                    'receipt_info_by_month': receipt_info_by_month,
                    'expenses': expenses,
                    'add_expense_form': add_expense_form,
                },
            )

    def post(self, request, *args, **kwargs):  # noqa: WPS210
        categories = ExpenseType.objects.filter(user=request.user).all()

        add_category_form = AddCategoryForm(request.POST)

        if add_category_form.is_valid():
            category_form = add_category_form.save(commit=False)
            category_form.user = request.user
            category_form.save()
            messages.success(request, 'Категория расхода успешно добавлена!')
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
        response_data = {}
        if add_expense_form.is_valid():
            expense = add_expense_form.save(commit=False)
            amount = add_expense_form.cleaned_data.get('amount')
            account = add_expense_form.cleaned_data.get('account')
            account_balance = get_object_or_404(Account, id=account.id)
            if account_balance.user == request.user:
                account_balance.balance -= amount
                account_balance.save()
                expense.user = request.user
                expense.save()
                messages.success(request, 'Операция расхода успешно добавлена!')
                response_data = {'success': True}
        else:
            response_data = {
                'success': False, 'errors': add_expense_form.errors,
            }
        return JsonResponse(response_data)


class ExpenseUpdateView(
    CustomNoPermissionMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = Expense
    template_name = 'expense/change_expense.html'
    form_class = AddExpenseForm
    no_permission_url = reverse_lazy('login')
    success_url = reverse_lazy(SuccessUrlView.EXPENSE_URL.value)

    def get(self, request, *args, **kwargs):
        expense = self.get_object()
        add_expense_form = AddExpenseForm(instance=expense)

        return render(
            request,
            self.template_name,
            {'add_expense_form': add_expense_form},
        )


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
            messages.success(self.request, 'Операция расхода успешно удалена!')
            return super().form_valid(form)


class ExpenseCategoryDeleteView(DeleteCategoryMixin):
    success_url = reverse_lazy(SuccessUrlView.EXPENSE_URL.value)

    def get_success_message(self):
        return 'Категория расхода успешно удалена!'

    def get_error_message(self):
        return 'Категория не может быть удалена, так как связана с одним из пунктом расхода'  # noqa: E501

    def delete_category(self):
        try:
            self.object.delete()
            return True
        except ProtectedError:
            return False
