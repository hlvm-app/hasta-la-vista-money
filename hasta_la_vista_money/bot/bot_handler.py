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
from hasta_la_vista_money.users.models import TelegramUser
from telebot import types


bot_admin.setup_middleware(AccessMiddleware())





def check_telegram_user(message):
    """
    Проверка существования телеграм пользователя в базе.

    :param telegram_user_id:
    :return:
    """
    telegram_user_id = message.from_user.id
    return TelegramUser.objects.filter(
        telegram_id=telegram_user_id,
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
    accounts = check_account_exist(user)
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
        message_id=pinned_message.id,
        disable_notification=True,
    )


@bot_admin.message_handler(commands=['select_account'])
def select_account(message):
    """
    Выбор счёта пользователем.

    :param message:
    :return:
    """
    telegram_user = check_telegram_user(message)
    user = telegram_user.user
    if telegram_user and check_account_exist(user):
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
    telegram_user = check_telegram_user(call)
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
    bot_admin.register_next_step_handler(message, get_date_receipt)


def get_date_receipt(message):
    try:
        date = parse(message.text)
        dictionary_string_from_qrcode['date'] = f'{date:%Y%m%dT%H%M%S}'
        bot_admin.send_message(message.chat.id, 'Введите сумму чека')
        bot_admin.register_next_step_handler(message, get_amount_receipt)
    except ParserError:
        bot_admin.send_message(
            message.chat.id,
            'Неверный формат даты! Повторите ввод сначала /manual',
        )


def get_amount_receipt(message):
    try:
        amount_receipt = message.text
        dictionary_string_from_qrcode['amount'] = decimal.Decimal(
            amount_receipt,
        )
        bot_admin.send_message(message.chat.id, 'Введите номер ФН')
        bot_admin.register_next_step_handler(message, get_fiscal_number_receipt)
    except ValueError:
        bot_admin.send_message(message.chat.id, 'Введите сумму!')


def get_fiscal_number_receipt(message):
    try:
        fn_receipt = message.text
        dictionary_string_from_qrcode['fn'] = int(fn_receipt)
        bot_admin.send_message(message.chat.id, 'Введите номер ФД')
        bot_admin.register_next_step_handler(message, get_fiscal_doc_receipt)
    except ValueError:
        bot_admin.send_message(message.chat.id, 'Введите корректный номер ФН!')


def get_fiscal_doc_receipt(message):
    try:
        fd_receipt = message.text
        dictionary_string_from_qrcode['fd'] = int(fd_receipt)
        bot_admin.send_message(message.chat.id, 'Введите номер ФП')
        bot_admin.register_next_step_handler(message, get_fp_receipt)
    except ValueError:
        bot_admin.send_message(message.chat.id, 'Введите корректный номер ФД!')


def get_fp_receipt(message):
    try:
        fp_receipt = message.text
        dictionary_string_from_qrcode['fp'] = int(fp_receipt)
        telegram_user_id = message.from_user.id

        telegram_user = check_telegram_user(telegram_user_id)

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


@bot_admin.message_handler(content_types=['text', 'document', 'photo'])
def handle_receipt(message):
    """
    Проверка того, зарегистрированный ли пользователь пишет боту.

    :param message:
    :return:
    """
    telegram_user = check_telegram_user(message)
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
