from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.bot.config_bot import bot_admin
from hasta_la_vista_money.bot.receipt_parser_json import handle_receipt_json
from hasta_la_vista_money.bot.receipt_parser_text import handle_receipt_text
from hasta_la_vista_money.bot.receipt_parser_text_qrcode import (
    handle_receipt_text_qrcode,
)
from hasta_la_vista_money.constants import TelegramMessage
from hasta_la_vista_money.users.models import TelegramUser, User
from telebot import types


@bot_admin.message_handler(commands=['auth'])
def handle_start(message):
    """
    Обработка команды /auth.

    :param message:
    :return:
    """
    telegram_username = message.from_user.username

    check_telegram_username = TelegramUser.objects.filter(
        username=telegram_username,
    ).first()

    if check_telegram_username:
        bot_admin.send_message(
            message.chat.id, TelegramMessage.ALREADY_LOGGED.value,
        )
    else:
        bot_admin.send_message(
            message.chat.id, TelegramMessage.REQUIRED_AUTHORIZATION.value,
        )
        bot_admin.register_next_step_handler(message, handle_auth)


def handle_auth(message):
    """
    Обработка логина и пароля от сайта для авторизации в боте.

    :param message:
    :return:
    """
    auth_data = message.text.split(':')
    if len(auth_data) != 2:
        bot_admin.reply_to(message, TelegramMessage.INCORRECT_FORMAT.value)
        return

    username, password = map(str, auth_data)
    user = User.objects.filter(username=username).first()
    telegram_username = message.from_user.username
    existing_telegram_user = TelegramUser.objects.filter(user=user).first()

    if user and user.check_password(password):
        check_existing_telegram_user(
            message, existing_telegram_user, telegram_username, user,
        )
    else:
        bot_admin.reply_to(
            message, TelegramMessage.INVALID_USERNAME_PASSWORD.value,
        )
        bot_admin.delete_message(message.from_user.id, message.message_id)


def check_existing_telegram_user(
    message, existing_telegram_user, telegram_username, user,
):
    """
    Проверка существования телеграм пользователя в базе данных.

    Если пользователь существует, то отправляется сообщение пользователю
    о том, что пользователь уже авторизован. В ином случае, создает запись
    в базе данных.

    :param message:
    :param existing_telegram_user:
    :param telegram_username:
    :param user:
    :return:
    """
    if existing_telegram_user:
        authenticated_user(message, existing_telegram_user)
    else:
        create_telegram_user(message, telegram_username, user)


def authenticated_user(message, existing_telegram_user):
    """
    Функция для проверки, авторизован ли пользователь в боте.

    :param message:
    :param existing_telegram_user:
    :return:
    """
    if existing_telegram_user.telegram_id == message.from_user.id:
        bot_admin.send_message(
            message.chat.id,
            TelegramMessage.ALREADY_LOGGING_LINK_ACCOUNT.value,
        )
        bot_admin.delete_message(message.from_user.id, message.message_id)
    else:
        bot_admin.send_message(
            message.chat.id,
            TelegramMessage.ALREADY_LINK_ANOTHER_ACCOUNT.value,
        )
        bot_admin.delete_message(message.from_user.id, message.message_id)


def create_telegram_user(message, telegram_username, user):
    """
    Создание записи в базе данных с данными о телеграм пользователе.

    :param message:
    :param telegram_username:
    :param user:
    :return:
    """
    TelegramUser.objects.create(
        user=user,
        username=telegram_username,
        telegram_id=message.from_user.id,
    )
    bot_admin.reply_to(
        message, TelegramMessage.AUTHORIZATION_SUCCESSFUL.value,
    )
    bot_admin.delete_message(message.from_user.id, message.message_id)


def check_account_exist(user):
    accounts = Account.objects.filter(user=user)
    if accounts.exists():
        markup = types.InlineKeyboardMarkup()
        for account in accounts:
            button = types.InlineKeyboardButton(
                text=account.name_account,
                callback_data=f'select_account_{account.id}',
            )
            markup.add(button)
        bot_admin.reply_to(message, 'Выберете счёт:', reply_markup=markup)
    else:
        bot_admin.reply_to(message, 'У вас нет доступных счетов.')


@bot_admin.message_handler(commands=['select_account'])
def select_account(message):
    """
    Выбор счёта пользователем.

    :param message:
    :return:
    """
    telegram_user_id = message.from_user.id

    telegram_user = TelegramUser.objects.filter(
        telegram_id=telegram_user_id,
    ).first()

    if telegram_user:
        user = telegram_user.user
        check_account_exist(user)
    else:
        bot_admin.reply_to(message, 'Вы не авторизованы.')


@bot_admin.callback_query_handler(func=lambda call: call.data.startswith(
    'select_account_',
))
def handle_select_account(call):
    """
    Обработка выбора счёта пользователем.

    :param call:
    :return:
    """
    account_id = int(call.data.split('_')[2])
    account = Account.objects.filter(id=account_id).first()
    if account:
        telegram_user_id = call.from_user.id
        telegram_user = TelegramUser.objects.filter(
            telegram_id=telegram_user_id,
        ).first()
        if telegram_user:
            telegram_user.selected_account_id = account_id
            telegram_user.save()
            bot_admin.send_message(
                call.message.chat.id, f'Выбран счёт: {account.name_account}',
            )
        else:
            bot_admin.send_message(
                call.message.chat.id, 'Ошибка: счёт не найден.',
            )


@bot_admin.message_handler(content_types=['text', 'document', 'photo'])
def handle_receipt(message):
    """
    Проверка того, зарегистрированный ли пользователь пишет боту.

    :param message:
    :return:
    """
    telegram_user_id = message.from_user.id

    telegram_user = TelegramUser.objects.filter(
        telegram_id=telegram_user_id,
    ).first()

    if telegram_user:
        user = telegram_user.user
        account = telegram_user.selected_account_id
        telegram_content_type(message, user, account)


def telegram_content_type(message, user, account):
    """
    Обработка сообщений по типу контента от пользователя.

    :param message:
    :param user:
    :param account:
    :return:
    """
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
