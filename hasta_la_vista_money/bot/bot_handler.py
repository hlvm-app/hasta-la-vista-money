from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.bot.handle_receipt_manual import HandleReceiptManual
from hasta_la_vista_money.bot.middleware import AccessMiddleware, bot_admin
from hasta_la_vista_money.bot.receipt_parser_json import handle_receipt_json
from hasta_la_vista_money.bot.receipt_parser_text import handle_receipt_text
from hasta_la_vista_money.bot.receipt_parser_text_qrcode import (
    handle_receipt_text_qrcode,
)
from hasta_la_vista_money.bot.services import get_telegram_user
from hasta_la_vista_money.constants import TelegramMessage
from hasta_la_vista_money.users.models import TelegramUser, User
from telebot import types

bot_admin.setup_middleware(AccessMiddleware())


@bot_admin.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot_admin.send_message(
        message.chat.id,
        ''.join(
            (
                'Описание команд:\n',
                '/start и /help выводят этот текст;\n',
                '/auth - позволяет авторизоваться в боте для доступа к ',
                'остальным командам.\n',
                '/select_account - выводит список счетов для выбора.\n',
                'Счета добавляются через сайт.\n',
                '/manual - позволяет добавить чек с помощью параметров ',
                'самого чека, если, например, QR-код не считывается.\n'
                '/deauthorize - отвязывает телеграм аккаунт от бота.',
            )
        )
    )


@bot_admin.message_handler(commands=['auth'])
def handle_start(message):
    """
    Обработка команды /auth.

    :param message:
    :return:
    """
    telegram_user = get_telegram_user(message)
    if telegram_user:
        bot_admin.send_message(
            message.chat.id,
            TelegramMessage.ALREADY_LOGGED.value,
        )
    else:
        bot_admin.send_message(
            message.chat.id,
            TelegramMessage.REQUIRED_AUTHORIZATION.value,
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

    if user and user.check_password(password):
        create_telegram_user(message, user)
    else:
        bot_admin.reply_to(
            message,
            TelegramMessage.INVALID_USERNAME_PASSWORD.value,
        )
        bot_admin.delete_message(message.from_user.id, message.message_id)


def create_telegram_user(message, user):
    """
    Создание записи в базе данных с данными о телеграм пользователе.

    :param message:
    :param user:
    :return:
    """
    TelegramUser.objects.create(
        user=user,
        username=message.from_user.username,
        telegram_id=message.from_user.id,
    )
    bot_admin.reply_to(
        message,
        TelegramMessage.AUTHORIZATION_SUCCESSFUL.value,
    )
    bot_admin.delete_message(message.from_user.id, message.message_id)


def check_account_exist(user):
    """
    Проверка существования счёта.

    :param user:
    :return:
    """
    return Account.objects.filter(user=user).first()


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


def pin_message(call, account):
    """
    Функция закрепления сообщения.

    :param call:
    :param account:
    :return:
    """
    bot_admin.unpin_all_chat_messages(chat_id=call.message.chat.id)
    pinned_message = bot_admin.send_message(
        chat_id=call.message.chat.id,
        text=f'Выбран счёт: {account.name_account}',
    )
    bot_admin.pin_chat_message(
        chat_id=call.message.chat.id,
        message_id=pinned_message.message_id,
        disable_notification=True,
    )


@bot_admin.message_handler(commands=['select_account'])
def select_account(message):
    """
    Выбор счёта пользователем.

    :param message:
    :return:
    """
    telegram_user = get_telegram_user(message)
    user = telegram_user.user
    if check_account_exist(user):
        markup = create_buttons_with_account(user)
        bot_admin.reply_to(message, 'Выберете счёт:', reply_markup=markup)
    else:
        bot_admin.reply_to(message, 'У вас нет доступных счетов.')


@bot_admin.callback_query_handler(
    func=lambda call: call.data.startswith(
        'select_account_',
    ),
)
def handle_select_account(call):
    """
    Обработка выбора счёта пользователем.

    :param call:
    :return:
    """
    telegram_user = get_telegram_user(call)
    account_id = int(call.data.split('_')[2])
    telegram_user.selected_account_id = account_id
    telegram_user.save()
    account = Account.objects.filter(id=account_id).first()
    pin_message(call, account)


@bot_admin.message_handler(commands=['manual'])
def start_process_add_manual_receipt(message):
    """
    Функция обработчик команды manual.

    :param message:
    :return:
    """
    bot_admin.send_message(
        message.chat.id,
        ''.join(
            (
                'Чтобы добавить чек используя данные с чека, ',
                'введите поочередно - Дату в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС, ',
                'сумму чека, ФН, ФД, ФП.<br>',
                'Сначала введите дату в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС',
            ),
        ),
    )
    receipt_manual = HandleReceiptManual(message)
    bot_admin.register_next_step_handler(
        message,
        receipt_manual.process_date_receipt,
    )


@bot_admin.message_handler(commands=['deauthorize'])
def process_deauthorize(message):
    """
    Функция отвязки телеграм аккаунта от аккаунта на сайте.

    :param message:
    :return:
    """
    TelegramUser.objects.get(telegram_id=message.from_user.id).delete()
    bot_admin.send_message(message.chat.id, 'Телеграм аккаунт отвязан!')


@bot_admin.message_handler(content_types=['text', 'document', 'photo'])
def handle_receipt(message):
    """
    Проверка того, зарегистрированный ли пользователь пишет боту.

    :param message:
    :return:
    """
    telegram_user = get_telegram_user(message)
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
