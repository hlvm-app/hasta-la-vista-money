from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.buttons_delete import (
    button_delete_category,
    button_delete_type_operation,
)
from hasta_la_vista_money.custom_mixin import CustomNoPermissionMixin
from hasta_la_vista_money.expense.forms import AddCategoryForm, AddExpenseForm
from hasta_la_vista_money.expense.models import Expense, ExpenseType
from hasta_la_vista_money.receipts.models import Receipt


class ExpenseView(CustomNoPermissionMixin, SuccessMessageMixin, TemplateView):
    model = Expense
    template_name = 'expense/expense.html'
    context_object_name = 'expense'
    no_permission_url = reverse_lazy('login')
    success_url = 'expense:list'

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
        if 'delete_expense_button' in request.POST:
            expense_id = request.POST.get('expense_id')
            button_delete_type_operation(
                model=Expense,
                request=request,
                object_id=expense_id,
                url=self.success_url,
            )
        if 'delete_category_expense_button' in request.POST:
            category_id = request.POST.get('category_expense_id')
            button_delete_category(
                model=ExpenseType,
                request=request,
                object_id=category_id,
                url=self.success_url,
            )

        categories = ExpenseType.objects.filter(user=request.user).all()
        add_expense_form = AddExpenseForm(request.POST)
        add_category_form = AddCategoryForm(request.POST)

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
                return redirect(self.success_url)
        elif add_category_form.is_valid():
            category_form = add_category_form.save(commit=False)
            category_form.user = request.user
            category_form.save()
            messages.success(request, 'Категория добавлена!')
            return redirect(self.success_url)
        else:
            return render(
                request,
                self.template_name,
                {
                    'add_category_form': add_category_form,
                    'categories': categories,
                    'add_expense_form': add_expense_form,
                },
            )
