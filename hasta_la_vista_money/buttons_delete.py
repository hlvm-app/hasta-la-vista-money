from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from hasta_la_vista_money.account.models import Account


def button_delete_receipt(model, request, object_id, url):
    receipt = get_object_or_404(model, pk=object_id)
    account = receipt.account
    amount_object = receipt.total_sum
    account_balance = get_object_or_404(Account, id=account.id)
    try:
        if account_balance.user == request.user:
            account_balance.balance += amount_object
            account_balance.save()

            for product in receipt.product.all():
                product.delete()
            receipt.customer.delete()

            receipt.delete()
            messages.success(request, 'Чек успешно удалён!')
            return redirect(reverse_lazy(url))
    except ProtectedError:
        messages.error(request, 'Чек не может быть удалён!')
        return redirect(reverse_lazy(url))


def button_delete_income(model, request, object_id, url):
    income = get_object_or_404(model, pk=object_id)
    account = income.account
    amount_object = income.amount
    account_balance = get_object_or_404(Account, id=account.id)
    if account_balance.user == request.user:
        account_balance.balance -= amount_object
        account_balance.save()
        try:
            income.delete()
            messages.success(request, 'Доходная операция успешно удалена!')
            redirect(reverse_lazy(url))
        except ProtectedError:
            messages.error(request, 'Доходная операция не может быть удалена!')
            return redirect(reverse_lazy(url))


def button_delete_expenses(model, request, object_id, url):
    expense = get_object_or_404(model, pk=object_id)
    account = expense.account
    amount_object = expense.amount
    account_balance = get_object_or_404(Account, id=account.id)
    if account_balance.user == request.user:
        account_balance.balance += amount_object
        account_balance.save()
        expense.delete()
        redirect(reverse_lazy(url))


def button_delete_account(model, request, object_id, url):
    account = get_object_or_404(model, pk=object_id)
    try:
        account.delete()
        messages.success(request, 'Счёт успешно удалён!')
        return redirect(reverse_lazy(url))
    except ProtectedError:
        messages.error(
            request,
            'Счёт не может быть удалён! Сначала '
            'вам необходимо удалить все чеки, '
            'доходы и расходы привязанные к счёту!',
        )
    redirect(reverse_lazy(url))


def button_delete_category_income(model, request, object_id, url):
    category = get_object_or_404(model, pk=object_id)
    try:
        category.delete()
        messages.success(request, 'Категория успешно удалена!')
        return redirect(reverse_lazy(url))
    except ProtectedError:
        messages.error(
            request,
            'Категория не может быть удалена! Сначала '
            'вам необходимо удалить все расходы или доходы, '
            'привязанные к категории!',
        )
        redirect(reverse_lazy(url))


def button_delete_category_expense(model, request, object_id, url):
    category = get_object_or_404(model, pk=object_id)
    try:
        category.delete()
        messages.success(request, 'Категория успешно удалена!')
        return redirect(reverse_lazy(url))
    except ProtectedError:
        messages.error(
            request,
            'Категория не может быть удалена! Сначала '
            'вам необходимо удалить все расходы или доходы, '
            'привязанные к категории!',
        )
        redirect(reverse_lazy(url))
