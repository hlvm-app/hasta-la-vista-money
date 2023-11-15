from django.contrib import messages
from django.db.models import Count, QuerySet, Sum
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.income.models import IncomeCategory
from hasta_la_vista_money.users.models import User


def build_category_tree(categories, parent_id=None, depth=2, current_depth=1):
    """Формирование дерева категория для отображения на сайте."""
    tree = []
    for category in categories:
        if category['parent_category'] == parent_id:
            children = []
            if current_depth < depth:
                children = build_category_tree(
                    categories,
                    category['id'],
                    depth,
                    current_depth + 1,
                )
            category_copy = category.copy()
            if children:
                category_copy['children'] = children
            tree.append(category_copy)
    return tree


def collect_info_receipt(user: User) -> QuerySet:
    """
    Сбор информации о чеках для отображения на страницах сайта.

    :param user: User
    :return: QuerySet
    """
    return (
        user.receipt_users.annotate(
            month=TruncMonth('receipt_date'),
        )
        .values(
            'month',
            'account__name_account',
        )
        .annotate(
            count=Count('id'),
            total_amount=Sum('total_sum'),
        )
        .order_by('-month')
    )


def create_object_view(form, request, message) -> JsonResponse:
    """
    Создание объектов для внесения данных по платежам кредита, расхода и дохода.

    :param form:
    :param request:
    :param message:
    :return: JsonResponse
    """
    response_data = {}
    if form.is_valid():
        form_instance = form.save(commit=False)
        cd = form.cleaned_data
        amount = cd.get('amount')
        account = cd.get('account')
        category_id = cd.get('category')
        selected_account = get_object_or_404(Account, id=account.id)
        selected_category = get_object_or_404(IncomeCategory, name=category_id)
        if selected_account.user == request.user:
            change_account_balance(account, request, amount)
            form_instance.user = request.user
            form_instance.category = selected_category
            form_instance.save()
            messages.success(
                request,
                message,
            )
            response_data = {'success': True}
    else:
        response_data = {
            'success': False,
            'errors': form.errors,
        }
    return JsonResponse(response_data)


def change_account_balance(account, request, amount):
    """Изменение баланса счёта."""
    if 'income' in request.path:
        account.balance += amount
    else:
        account.balance -= amount
    account.save()
