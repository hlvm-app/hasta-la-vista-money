from hasta_la_vista_money.account.models import Account
from telebot import types


def create_buttons_with_account(user):
    """
    Функция создания кнопок со счетами.

    :param user:
    :return:
    """
    accounts = Account.objects.filter(user=user)
    markup = types.InlineKeyboardMarkup()
    for account in accounts:
        button = types.InlineKeyboardButton(
            text=account.name_account,
            callback_data=f'select_account_{account.id}',
        )
        markup.add(button)
    return markup
