import decimal

from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from hasta_la_vista_money import constants
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.bot.json_parser.json_parser import JsonParser
from hasta_la_vista_money.bot.log_config import logger
from hasta_la_vista_money.bot.receipt_handler.data_classes import (
    CustomerData,
    ProductData,
    ReceiptData,
    ReceiptDataWriter,
)
from hasta_la_vista_money.bot.receipt_handler.receipt_parse_handler import (
    check_exists_number_receipt,
    check_operation_type,
    get_string_result_receipt,
    handle_integrity_error,
)
from hasta_la_vista_money.bot.send_message.send_message_tg_user import (
    SendMessageToTelegramUser,
)
from hasta_la_vista_money.bot.services import convert_date_time, convert_number
from hasta_la_vista_money.users.models import User


class ReceiptParser:
    """
    Класс парсинга чека.

    АТРИБУТЫ:

    json_data: dict
        Принимает словарь.
    parser: class
        Экземпляр класса JsonParser.
    customer: class
        Объект модели Customer.
    receipt: class
        Объект модели Receipt.
    product_list: list
        Список продуктов.

    МЕТОДЫ:

    parse_products() -> None
        Метод класса для парсинга продуктов из JSON данных чека.
        Парсинг включает в себя название продукта, его цену, количество и сумму.
        Также, тип НДС (10%, 20%) и сумма НДС по каждому товару.

    parse_customer() -> None
        Метод класса для парсинга продавца из JSON данных чека.
        Парсинг включает в себя название продавца, например: ООО 'Пятерочка'.
        Фактический адрес расположения магазина, в котором был распечатан чек.
        Название того магазина, где был распечатан чек.

    parse_receipt(chat_id: int) -> None
        Метод класса для парсинга основной информации о чеке.
        Парсится дата чека, номер, тип операции(Приход, расход и пр.) и итоговая
        сумма.
        В методе также проверяется существование номера чека в базе данных,
        чтобы исключить дубли.
        По итогу, если чек существует или был добавлен, отправляется
        сообщение тому пользователю, кто попытался добавить чек.

    """

    def __init__(self, json_data, user, account):
        """Метод-конструктор инициализирующий аргумент json_data."""
        self.json_data: [list | dict] = json_data
        self.user: User = user
        self.account: Account = account
        self.parser = JsonParser(self.json_data)
        self.customer = None
        self.receipt = None
        self.product_list = []

    def parse_products(self) -> None:
        """
        Метод класса для парсинга продуктов из JSON данных чека.

        Парсинг включает в себя название продукта, его цену, количество и сумму.
        Также, тип НДС (10%, 20%) и сумма НДС по каждому товару.
        """
        try:
            products_list = self.parser.parse_json(
                self.json_data,
                constants.ITEMS_PRODUCT,
            )
            for product in products_list:
                product_name = self.parser.parse_json(
                    product,
                    constants.PRODUCT_NAME,
                )
                price = convert_number(
                    self.parser.parse_json(
                        product,
                        constants.PRICE,
                    ),
                )
                quantity = self.parser.parse_json(
                    product,
                    constants.QUANTITY,
                )
                amount = convert_number(
                    self.parser.parse_json(
                        product,
                        constants.AMOUNT,
                    ),
                )
                nds_type = self.parser.parse_json(
                    product,
                    constants.NDS_TYPE,
                )
                nds_sum = convert_number(
                    self.parser.parse_json(
                        product,
                        constants.NDS_SUM,
                    ),
                )

                product_data = ProductData(
                    user=self.user,
                    product_name=product_name,
                    price=price,
                    quantity=quantity,
                    amount=amount,
                    nds_type=nds_type,
                    nds_sum=nds_sum,
                )
                products = ReceiptDataWriter.create_product(product_data)
                self.product_list.append(products)
            self.receipt.product.set(self.product_list)
        except IntegrityError as integrity_error:
            logger.error(
                f'Ошибка записи товаров в базу данных: {integrity_error}',
            )

    def parse_customer(self) -> None:
        """
        Метод класса для парсинга продавца из JSON данных чека.

        Парсинг включает в себя название продавца, например: ООО 'Пятерочка'.
        Фактический адрес расположения магазина, в котором был распечатан чек.
        Название того магазина, где был распечатан чек.
        """
        try:
            name_seller = self.parser.parse_json(
                self.json_data,
                constants.NAME_SELLER,
            )
            retail_place_address = self.parser.parse_json(
                self.json_data,
                constants.RETAIL_PLACE_ADDRESS,
            )
            retail_place = self.parser.parse_json(
                self.json_data,
                constants.RETAIL_PLACE,
            )

            customer_data = CustomerData(
                user=self.user,
                name_seller=name_seller,
                retail_place_address=retail_place_address,
                retail_place=retail_place,
            )
            self.customer = ReceiptDataWriter.create_customer(customer_data)
        except IntegrityError as integrity_error:
            logger.error(
                f'Ошибка записи продавца в базу данных: {integrity_error}',
            )

    def parse_receipt(
        self,
        chat_id: int,
    ) -> None:
        """
        Метод класса для парсинга основной информации о чеке.

        Парсится дата чека, номер, тип операции(Приход, расход и пр.) и итоговая
        сумма.

        В методе также проверяется существование номера чека в базе данных,
        чтобы исключить дубли.
        По итогу, если чек существует или был добавлен, отправляется
        сообщение тому пользователю, кто попытался добавить чек.

        :param chat_id: ID пользователя, кому направлять сообщения.


        """
        try:
            (
                receipt_date,
                number_receipt,
                nds10,
                nds20,
                operation_type,
                total_sum,
            ) = self.extract_receipt_info()

            total_sum = check_operation_type(operation_type, total_sum)

            check_number_receipt = check_exists_number_receipt(
                user=self.user,
                number_receipt=number_receipt,
            )

            if check_number_receipt is None:
                self.process_receipt_data(
                    receipt_date,
                    number_receipt,
                    nds10,
                    nds20,
                    operation_type,
                    total_sum,
                )
                SendMessageToTelegramUser.send_message_to_telegram_user(
                    chat_id,
                    get_string_result_receipt(
                        account=self.account,
                        product_list=self.product_list,
                        receipt_date=self.receipt.receipt_date,
                        customer=self.customer,
                        total_sum=total_sum,
                    ),
                )
            else:
                SendMessageToTelegramUser.send_message_to_telegram_user(
                    chat_id,
                    _(constants.RECEIPT_ALREADY_EXISTS),
                )
                return

        except IntegrityError as integrity_error:
            handle_integrity_error(
                chat_id=chat_id,
                integrity_error=integrity_error,
            )
        except Http404:
            SendMessageToTelegramUser.send_message_to_telegram_user(
                chat_id,
                constants.NOT_CREATE_ACCOUNT,
            )

    def process_receipt_data(
        self,
        receipt_date,
        number_receipt,
        nds10,
        nds20,
        operation_type,
        total_sum,
    ):
        if 'query' in self.json_data and number_receipt is None:
            logger.error(constants.RECEIPT_NOT_ACCEPTED)
            return
        self.parse_customer()
        account_balance = get_object_or_404(Account, id=self.account)
        if account_balance.user == self.user:
            account_balance.balance -= decimal.Decimal(total_sum)
            account_balance.save()
        receipt_data = ReceiptData(
            user=self.user,
            account=account_balance,
            receipt_date=receipt_date,
            number_receipt=number_receipt,
            nds10=nds10,
            nds20=nds20,
            operation_type=operation_type,
            total_sum=total_sum,
            customer=self.customer,
        )
        self.receipt = ReceiptDataWriter.create_receipt(receipt_data)
        self.parse_products()

    def extract_receipt_info(self):
        receipt_date = convert_date_time(
            self.parser.parse_json(
                self.json_data,
                constants.RECEIPT_DATE_TIME,
            ),
        )
        number_receipt = self.parser.parse_json(
            self.json_data,
            constants.NUMBER_RECEIPT,
        )

        nds10 = convert_number(
            self.parser.parse_json(
                self.json_data,
                constants.NDS10,
            ),
        )

        nds20 = convert_number(
            self.parser.parse_json(
                self.json_data,
                constants.NDS20,
            ),
        )

        operation_type = self.parser.parse_json(
            self.json_data,
            constants.OPERATION_TYPE,
        )
        total_sum = convert_number(
            self.parser.parse_json(
                self.json_data,
                constants.TOTAL_SUM,
            ),
        )
        return (
            receipt_date,
            number_receipt,
            nds10,
            nds20,
            operation_type,
            total_sum,
        )
