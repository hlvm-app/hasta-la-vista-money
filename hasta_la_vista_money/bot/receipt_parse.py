import decimal

from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.bot.config_bot import bot_admin
from hasta_la_vista_money.bot.json_parse import JsonParser
from hasta_la_vista_money.bot.log_config import logger
from hasta_la_vista_money.bot.services import convert_date_time, convert_number
from hasta_la_vista_money.constants import ReceiptConstants, TelegramMessage
from hasta_la_vista_money.receipts.models import Customer, Product, Receipt


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
        Парсинг включает в себя название продавца, например: ООО "Пятерочка".
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

    parse(chat_id) -> None
        Метод отвечает за вызов метода по парсингу чека.
        В случае ошибки выбрасывает исключение и отправляет ошибку пользователю.
    """

    def __init__(self, json_data, user, account):
        """Метод-конструктор инициализирующий аргумент json_data."""
        self.json_data = json_data
        self.user = user
        self.account = account
        self.parser = JsonParser(self.json_data)
        self.customer = None
        self.receipt = None
        self.product_list = []

    def parse_products(self) -> None:  # noqa: WPS210
        """
        Метод класса для парсинга продуктов из JSON данных чека.

        Парсинг включает в себя название продукта, его цену, количество и сумму.
        Также, тип НДС (10%, 20%) и сумма НДС по каждому товару.
        """
        try:
            products_list = self.parser.parse_json(
                self.json_data, ReceiptConstants.ITEMS_PRODUCT.value,
            )
            for product in products_list:
                product_name = self.parser.parse_json(
                    product, ReceiptConstants.PRODUCT_NAME.value,
                )
                price = convert_number(
                    self.parser.parse_json(
                        product, ReceiptConstants.PRICE.value,
                    ),
                )
                quantity = self.parser.parse_json(
                    product, ReceiptConstants.QUANTITY.value,
                )
                amount = convert_number(self.parser.parse_json(
                    product, ReceiptConstants.AMOUNT.value,
                ))
                nds_type = self.parser.parse_json(
                    product, ReceiptConstants.NDS_TYPE.value,
                )
                nds_sum = convert_number(self.parser.parse_json(
                    product, ReceiptConstants.NDS_SUM.value,
                ))

                products = ReceiptDataWriter.create_product(
                    user=self.user,
                    product_name=product_name,
                    price=price,
                    quantity=quantity,
                    amount=amount,
                    nds_type=nds_type,
                    nds_sum=nds_sum,
                )
                self.product_list.append(products)
            self.receipt.product.set(self.product_list)
        except IntegrityError as integrity_error:
            logger.error(
                f'Ошибка записи товаров в базу данных: {integrity_error}',
            )

    def parse_customer(self) -> None:
        """
        Метод класса для парсинга продавца из JSON данных чека.

        Парсинг включает в себя название продавца, например: ООО "Пятерочка".
        Фактический адрес расположения магазина, в котором был распечатан чек.
        Название того магазина, где был распечатан чек.
        """
        try:
            name_seller = self.parser.parse_json(
                self.json_data, ReceiptConstants.NAME_SELLER.value,
            )
            retail_place_address = self.parser.parse_json(
                self.json_data, ReceiptConstants.RETAIL_PLACE_ADDRESS.value,
            )
            retail_place = self.parser.parse_json(
                self.json_data, ReceiptConstants.RETAIL_PLACE.value,
            )
            self.customer = ReceiptDataWriter.create_customer(
                user=self.user,
                name_seller=name_seller,
                retail_place_address=retail_place_address,
                retail_place=retail_place,
            )
        except IntegrityError as integrity_error:
            logger.error(
                f'Ошибка записи продавца в базу данных: {integrity_error}',
            )

    def parse_receipt(self, chat_id: int) -> None:  # noqa: WPS231 C901 WPS210 WPS213 E501
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
            receipt_date = convert_date_time(self.parser.parse_json(
                self.json_data, ReceiptConstants.RECEIPT_DATE_TIME.value,
            ))
            number_receipt = self.parser.parse_json(
                self.json_data, ReceiptConstants.NUMBER_RECEIPT.value,
            )

            operation_type = self.parser.parse_json(
                self.json_data, ReceiptConstants.OPERATION_TYPE.value,
            )
            total_sum = convert_number(self.parser.parse_json(
                self.json_data, ReceiptConstants.TOTAL_SUM.value,
            ))

            if operation_type in {2, 3}:
                total_sum = -total_sum

            check_number_receipt = Receipt.objects.filter(
                user=self.user,
                number_receipt=number_receipt,
            ).first()

            if 'query' in self.json_data and number_receipt is None:
                logger.error(ReceiptConstants.RECEIPT_NOT_ACCEPTED.value)
                return
            elif check_number_receipt:
                bot_admin.send_message(
                    chat_id, ReceiptConstants.RECEIPT_ALREADY_EXISTS.value,
                )
                return
            else:
                self.parse_customer()
                account_balance = get_object_or_404(Account, id=self.account)
                if account_balance.user == self.user:
                    account_balance.balance -= decimal.Decimal(total_sum)
                    account_balance.save()
                self.receipt = ReceiptDataWriter.create_receipt(
                    user=self.user,
                    account=account_balance,
                    receipt_date=receipt_date,
                    number_receipt=number_receipt,
                    operation_type=operation_type,
                    total_sum=total_sum,
                    customer=self.customer,
                )
                self.parse_products()
                bot_admin.send_message(
                    chat_id, ReceiptConstants.RECEIPT_BE_ADDED.value,
                )
        except IntegrityError as integrity_error:
            if 'account' in str(integrity_error):
                logger.error(TelegramMessage.NOT_CREATE_ACCOUNT.value)
            else:
                logger.error(TelegramMessage.ERROR_DATABASE_RECORD.value)
        except Http404:
            logger.error(TelegramMessage.NOT_CREATE_ACCOUNT.value)

    def parse(self, chat_id: int) -> None:
        """
        Метод отвечает за вызов метода `parse_receipt` по парсингу чека.

        В случае ошибки выбрасывает исключение и отправляет ошибку пользователю.

        :argument chat_id: ID пользователя, кому направлять сообщения.


        """
        self.parse_receipt(chat_id)


class ReceiptDataWriter:
    @classmethod
    def create_product(  # noqa: WPS211
        cls,
        user,
        product_name,
        price,
        quantity,
        amount,
        nds_type,
        nds_sum,
    ):
        return Product.objects.create(
            user=user,
            product_name=product_name,
            price=price,
            quantity=quantity,
            amount=amount,
            nds_type=nds_type,
            nds_sum=nds_sum,
        )

    @classmethod
    def create_customer(  # noqa: WPS211
        cls,
        user,
        name_seller,
        retail_place_address,
        retail_place,
    ):
        return Customer.objects.create(
            user=user,
            name_seller=name_seller,
            retail_place_address=retail_place_address,
            retail_place=retail_place,
        )

    @classmethod
    def create_receipt(  # noqa: WPS211
        cls,
        user,
        account,
        receipt_date,
        number_receipt,
        operation_type,
        total_sum,
        customer,
    ):
        return Receipt.objects.create(
            user=user,
            account=account,
            receipt_date=receipt_date,
            number_receipt=number_receipt,
            operation_type=operation_type,
            total_sum=total_sum,
            customer=customer,
        )
