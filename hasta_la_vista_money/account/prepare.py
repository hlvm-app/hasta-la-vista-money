from operator import itemgetter

from hasta_la_vista_money.users.models import User


def collect_info_income(user: User):
    """
    Сбор информации о доходах из базы данных, фильтруемая по пользователю.

    :param user: User
    :return: Queryset
    """
    return user.income_users.select_related('user').values(
        'id',
        'date',
        'account__name_account',
        'category__name',
        'amount',
    )


def collect_info_expense(user: User):
    """
    Сбор информации о расходах из базы данных, фильтруемая по пользователю.

    :param user: User
    :return: Queryset
    """
    return user.expense_users.select_related('user').values(
        'id',
        'date',
        'account__name_account',
        'category__name',
        'amount',
    )


def sort_expense_income(expenses, income):
    """
    Создание отсортированного списка с расходам и доходами.

    :param expenses: Queryset
    :param income: Queryset
    :return: list
    """
    return sorted(
        list(expenses) + list(income),
        key=itemgetter('date'),
        reverse=True,
    )
