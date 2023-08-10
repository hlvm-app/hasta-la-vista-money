import decimal

from dateutil.parser import ParserError, parse
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.bot.middleware import AccessMiddleware, bot_admin
from hasta_la_vista_money.bot.receipt_api_receiver import ReceiptApiReceiver
from hasta_la_vista_money.bot.receipt_parse import ReceiptParser
from hasta_la_vista_money.bot.receipt_parser_json import handle_receipt_json
from hasta_la_vista_money.bot.receipt_parser_text import handle_receipt_text
from hasta_la_vista_money.bot.receipt_parser_text_qrcode import (
    handle_receipt_text_qrcode,
)
from hasta_la_vista_money.constants import TelegramMessage
from hasta_la_vista_money.users.models import TelegramUser, User
from telebot import types

bot_admin.setup_middleware(AccessMiddleware())


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


def get_telegram_user(message):
    """
    Функция получения о наличии телеграм пользователя в базе данных.

    :param message:
    :return:
    """
    return TelegramUser.objects.filter(
        telegram_id=message.from_user.id,
    ).first()


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


dictionary_string_from_qrcode = {}


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
                'введите поочередно - дату, ФД, ФП и номер чека. ',
                'Сначала введите дату в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС',
            ),
        ),
    )
    bot_admin.register_next_step_handler(message, process_date_receipt)


def process_date_receipt(message):
    """
    Получение даты от пользователя.

    :param message:
    :return:
    """
    try:
        date = parse(message.text)
        dictionary_string_from_qrcode['date'] = f'{date:%Y%m%dT%H%M%S}'
        bot_admin.send_message(message.chat.id, 'Введите сумму чека')
        bot_admin.register_next_step_handler(message, process_amount_receipt)
    except ParserError:
        bot_admin.send_message(
            message.chat.id,
            'Неверный формат даты! Повторите ввод сначала /manual',
        )


def process_amount_receipt(message):
    """
    Получение суммы от пользователя.

    :param message:
    :return:
    """
    try:
        amount_receipt = message.text
        dictionary_string_from_qrcode['amount'] = decimal.Decimal(
            amount_receipt,
        )
        bot_admin.send_message(message.chat.id, 'Введите номер ФН')
        bot_admin.register_next_step_handler(
            message,
            process_fiscal_number_receipt,
        )
    except ValueError:
        bot_admin.send_message(message.chat.id, 'Введите сумму!')


def process_fiscal_number_receipt(message):
    """
    Получение ФН от пользователя.

    :param message:
    :return:
    """
    try:
        fn_receipt = message.text
        dictionary_string_from_qrcode['fn'] = int(fn_receipt)
        bot_admin.send_message(message.chat.id, 'Введите номер ФД')
        bot_admin.register_next_step_handler(
            message,
            process_fiscal_doc_receipt,
        )
    except ValueError:
        bot_admin.send_message(message.chat.id, 'Введите корректный номер ФН!')


def process_fiscal_doc_receipt(message):
    """
    Получение ФД от пользователя.

    :param message:
    :return:
    """
    try:
        fd_receipt = message.text
        dictionary_string_from_qrcode['fd'] = int(fd_receipt)
        bot_admin.send_message(message.chat.id, 'Введите номер ФП')
        bot_admin.register_next_step_handler(message, process_fp_receipt)
    except ValueError:
        bot_admin.send_message(message.chat.id, 'Введите корректный номер ФД!')


def process_fp_receipt(message):
    """
    Получение ФП от пользователя.

    :param message:
    :return:
    """
    try:
        fp_receipt = message.text
        dictionary_string_from_qrcode['fp'] = int(fp_receipt)
        telegram_user_id = message.from_user.id

        telegram_user = get_telegram_user(telegram_user_id)

        if telegram_user:
            user = telegram_user.user
            account = telegram_user.selected_account_id
            client = ReceiptApiReceiver()
            json_data = client.get_receipt(
                ''.join(
                    (
                        f't={dictionary_string_from_qrcode["date"]}',
                        f'&s={dictionary_string_from_qrcode["amount"]}',
                        f'&fn={dictionary_string_from_qrcode["fn"]}',
                        f'&i={dictionary_string_from_qrcode["fd"]}',
                        f'&fp={dictionary_string_from_qrcode["fp"]}&n=1',
                    ),
                ),
            )
            parser = ReceiptParser(json_data, user, account)
            parser.parse(message.chat.id)
    except ValueError:
        bot_admin.send_message(message.chat.id, 'Введите корректный номер ФП!')


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
