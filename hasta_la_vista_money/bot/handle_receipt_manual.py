import decimal

from dateutil.parser import ParserError, parse
from hasta_la_vista_money.bot.config_bot.config_bot import bot_admin
from hasta_la_vista_money.bot.receipt_api_receiver import ReceiptApiReceiver
from hasta_la_vista_money.bot.receipt_parse import ReceiptParser
from hasta_la_vista_money.bot.send_message.send_message_tg_user import (
    SendMessageToTelegramUser,
)
from hasta_la_vista_money.bot.services import get_telegram_user


class HandleReceiptManual:
    def __init__(self, message):
        """
        Конструктов класса инициализирующий аргументы класса.

        :param message:
        """
        self.message = message
        self.dictionary_string_from_qrcode = {}

    def process_date_receipt(self, message):
        """
        Получение даты от пользователя.

        :param message:
        :return:
        """
        try:
            date = parse(message.text)
            self.dictionary_string_from_qrcode['date'] = f'{date:%Y%m%dT%H%M%S}'
            SendMessageToTelegramUser.send_message_to_telegram_user(
                message.chat.id,
                'Введите сумму чека',
            )
            bot_admin.register_next_step_handler(
                message,
                self.process_amount_receipt,
            )
        except ParserError:
            SendMessageToTelegramUser.send_message_to_telegram_user(
                message.chat.id,
                'Неверный формат даты! Повторите ввод сначала /manual',
            )

    def process_amount_receipt(self, message):
        """
        Получение суммы от пользователя.

        :param message:
        :return:
        """
        try:
            amount_receipt = message.text
            self.dictionary_string_from_qrcode['amount'] = decimal.Decimal(
                amount_receipt,
            )
            SendMessageToTelegramUser.send_message_to_telegram_user(
                message.chat.id,
                'Введите номер ФН',
            )
            bot_admin.register_next_step_handler(
                message,
                self.process_fiscal_number_receipt,
            )
        except ValueError:
            SendMessageToTelegramUser.send_message_to_telegram_user(
                message.chat.id,
                'Введите сумму!',
            )

    def process_fiscal_number_receipt(self, message):
        """
        Получение ФН от пользователя.

        :param message:
        :return:
        """
        try:
            fn_receipt = message.text
            self.dictionary_string_from_qrcode['fn'] = int(fn_receipt)
            SendMessageToTelegramUser.send_message_to_telegram_user(
                message.chat.id,
                'Введите номер ФД',
            )
            bot_admin.register_next_step_handler(
                message,
                self.process_fiscal_doc_receipt,
            )
        except ValueError:
            SendMessageToTelegramUser.send_message_to_telegram_user(
                message.chat.id,
                'Введите корректный номер ФН!',
            )

    def process_fiscal_doc_receipt(self, message):
        """
        Получение ФД от пользователя.

        :param message:
        :return:
        """
        try:
            fd_receipt = message.text
            self.dictionary_string_from_qrcode['fd'] = int(fd_receipt)
            SendMessageToTelegramUser.send_message_to_telegram_user(
                message.chat.id,
                'Введите номер ФП',
            )
            bot_admin.register_next_step_handler(
                message,
                self.process_fp_receipt,
            )
        except ValueError:
            SendMessageToTelegramUser.send_message_to_telegram_user(
                message.chat.id,
                'Введите корректный номер ФД!',
            )

    def process_fp_receipt(self, message):
        """
        Получение ФП от пользователя.

        :param message:
        :return:
        """
        try:
            fp_receipt = message.text
            self.dictionary_string_from_qrcode['fp'] = int(fp_receipt)

            telegram_user = get_telegram_user(message)

            if telegram_user:
                user = telegram_user.user
                account = telegram_user.selected_account_id
                client = ReceiptApiReceiver()
                json_data = client.get_receipt(
                    ''.join(
                        (
                            f't={self.dictionary_string_from_qrcode["date"]}',
                            f'&s={self.dictionary_string_from_qrcode["amount"]}',  # noqa: E501
                            f'&fn={self.dictionary_string_from_qrcode["fn"]}',
                            f'&i={self.dictionary_string_from_qrcode["fd"]}',
                            f'&fp={self.dictionary_string_from_qrcode["fp"]}&n=1',  # noqa: E501
                        ),
                    ),
                )
                parser = ReceiptParser(json_data, user, account)
                parser.parse_receipt(message.chat.id)
        except ValueError:
            SendMessageToTelegramUser.send_message_to_telegram_user(
                message.chat.id,
                'Введите корректный номер ФП!',
            )
