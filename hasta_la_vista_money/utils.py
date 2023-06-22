from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from hasta_la_vista_money.account.models import Account


def button_delete_receipt(model, request, object_id, url):
    name_model = get_object_or_404(model, pk=object_id)
    account = name_model.account
    amount_object = name_model.total_sum
    account_balance = get_object_or_404(Account, id=account.id)
    try:
        if account_balance.user == request.user:
            account_balance.balance += amount_object
            account_balance.save()

            for product in name_model.product.all():
                product.delete()
            name_model.customer.delete()

            name_model.delete()
            messages.success(request, 'Чек успешно удалён!')
            return redirect(reverse_lazy(url))
    except ProtectedError:
        messages.error(request, 'Чек не может быть удалён!')
        return redirect(reverse_lazy(url))


def button_delete_income(model, request, object_id, url):
    name_model = get_object_or_404(model, pk=object_id)
    account = name_model.account
    amount_object = name_model.amount
    account_balance = get_object_or_404(Account, id=account.id)
    if account_balance.user == request.user:
        account_balance.balance -= amount_object
        account_balance.save()
        try:
            name_model.delete()
            messages.success(request, 'Доходная операция успешно удалена!')
            redirect(reverse_lazy(url))
        except ProtectedError:
            messages.error(request, 'Доходная операция не может быть удалена!')
            return redirect(reverse_lazy(url))


def button_delete_expenses(model, request, object_id, url):
    name_model = get_object_or_404(model, pk=object_id)
    account = name_model.account
    amount_object = name_model.amount
    account_balance = get_object_or_404(Account, id=account.id)
    if account_balance.user == request.user:
        account_balance.balance += amount_object
        account_balance.save()
        name_model.delete()
        redirect(reverse_lazy(url))


def button_delete_account(model, request, object_id, url):
    name_model = get_object_or_404(model, pk=object_id)
    try:
        name_model.delete()
        return redirect(reverse_lazy(url))
    except ProtectedError:
        messages.error(
            request,
            'Счёт не может быть удалён! Сначала '
            'вам необходимо удалить все чеки, '
            'доходы и расходы привязанные к счёту!',
        )
    redirect(reverse_lazy(url))
