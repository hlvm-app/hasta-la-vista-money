from telebot import types

from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.bot.config_bot import bot_admin
from hasta_la_vista_money.bot.receipt_parser_json import handle_receipt_json
from hasta_la_vista_money.bot.receipt_parser_text import handle_receipt_text
from hasta_la_vista_money.bot.receipt_parser_text_qrcode import (
    handle_receipt_text_qrcode,
)
from hasta_la_vista_money.constants import TelegramMessage
from hasta_la_vista_money.users.models import TelegramUser, User


@bot_admin.message_handler(commands=['auth'])
def handle_start(message):
    bot_admin.send_message(
        message.chat.id, TelegramMessage.REQUIRED_AUTHORIZATION.value,
    )
    bot_admin.register_next_step_handler(message, handle_auth)


def handle_auth(message):  # noqa: WPS210
    auth_data = message.text.split(':')
    if len(auth_data) == 2:
        username = auth_data[0].strip()
        password = auth_data[1].strip()
        user = User.objects.filter(username=username).first()
        telegram_username = message.from_user.username

        if user and user.check_password(password):
            existing_telegram_user = TelegramUser.objects.filter(
                user=user,
            ).first()
            if existing_telegram_user:
                if existing_telegram_user.telegram_id == message.from_user.id:
                    bot_admin.reply_to(
                        message,
                        TelegramMessage.ALREADY_LOGGING_LINK_ACCOUNT.value,
                    )
                else:
                    bot_admin.reply_to(
                        message,
                        TelegramMessage.ALREADY_LINK_ANOTHER_ACCOUNT.value,
                    )
            else:
                TelegramUser.objects.create(
                    user=user,
                    username=telegram_username,
                    telegram_id=message.from_user.id,
                )
                bot_admin.reply_to(
                    message, TelegramMessage.AUTHORIZATION_SUCCESSFUL.value,
                )
        else:
            bot_admin.reply_to(
                message, TelegramMessage.INVALID_USERNAME_PASSWORD.value,
            )
    else:
        bot_admin.reply_to(message, TelegramMessage.INCORRECT_FORMAT.value)


@bot_admin.message_handler(commands=['select_account'])
def select_account(message):
    telegram_user_id = message.from_user.id

    telegram_user = TelegramUser.objects.filter(
        telegram_id=telegram_user_id,
    ).first()

    if telegram_user:
        user = telegram_user.user
        accounts = Account.objects.filter(user=user)
        if accounts.exists():
            markup = types.InlineKeyboardMarkup()
            for account in accounts:
                button = types.InlineKeyboardButton(
                    text=account.name_account,
                    callback_data=f'select_account_{account.id}'
                )
                markup.add(button)
            bot_admin.reply_to(message, 'Выберете счёт:', reply_markup=markup)
        else:
            bot_admin.reply_to(message, 'У вас нет доступных счетов.')
    else:
        bot_admin.reply_to(message, 'Вы не авторизованы.')


@bot_admin.callback_query_handler(func=lambda call: call.data.startswith('select_account_'))
def handle_select_account(call):
    account_id = int(call.data.split('_')[2])
    account = Account.objects.filter(id=account_id).first()
    if account:
        telegram_user_id = call.from_user.id
        telegram_user = TelegramUser.objects.filter(telegram_id=telegram_user_id).first()
        if telegram_user:
            telegram_user.selected_account_id = account_id
            telegram_user.save()
            bot_admin.send_message(call.message.chat.id, f'Выбран счёт: {account.name_account}')
        else:
            bot_admin.send_message(call.message.chat.id, 'Ошибка: счёт не найден.')


@bot_admin.message_handler(content_types=['text', 'document', 'photo'])
def handle_receipt(message):
    telegram_user_id = message.from_user.id

    telegram_user = TelegramUser.objects.filter(
        telegram_id=telegram_user_id,
    ).first()

    if telegram_user:
        user = telegram_user.user
        account = telegram_user.selected_account_id

        if message.content_type == 'text':
            handle_receipt_text(message, bot_admin, user, account)
        elif message.content_type == 'photo':
            handle_receipt_text_qrcode(message, bot_admin, user, account)
        elif message.content_type == 'document':
            handle_receipt_json(message, bot_admin, user, account)
        else:
            bot_admin.send_message(
                message.chat.id,
                TelegramMessage.ACCEPTED_FORMAT_JSON.value,
            )
