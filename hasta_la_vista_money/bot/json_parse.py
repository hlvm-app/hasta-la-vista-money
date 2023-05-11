"""Модуль разбора json данных."""

import datetime

from django.db import IntegrityError
from hasta_la_vista_money.bot.config_bot import bot_admin
from hasta_la_vista_money import constants
from hasta_la_vista_money.bot.log_config import logger
from hasta_la_vista_money.bot.services import convert_date_time, convert_number
from hasta_la_vista_money.receipts.models import Customer, Product, Receipt


class JsonParser:
    """
    Универсальный класс разбора json данных.

    АТРИБУТЫ:

    json_data: dict
        Словарь с данными.

    МЕТОДЫ:

    parse_json(json_data: dict, key: str) -> list[dict] | int | str | None
        Метод разбора json данных.
        Принимает словарь и ключ для поиска значения в переданном словаре.

    __get_value(dictionary, key) -> str | list | int | None)
        Приватный метод получения значений из словаря (json данных).
    """

    def __init__(self, json_data):
        """Метод-конструктор инициализирующий аргумент json_data."""
        self.json_data = json_data

    def parse_json(
        self, json_data: dict, key: str,
    ) -> list[dict] | int | str | None:
        """
        Метод разбора json данных.

        Принимает словарь и ключ для поиска значения в переданном словаре.

        АРГУМЕНТЫ:

        json_data: dict
            Принимает словарь.

        key: str
            Ключ для поиска в словаре.

        ВОЗВРАЩАЕТ:

        list[dict] | None
            Словарь внутри списка, либо None
        """
        return JsonParser.__get_value(self, json_data, key)

    def __get_value(  # noqa: WPS112
        self, dictionary, key,
    ) -> str | list | int | None:
        """
        Приватный метод получения значений из словаря (json данных).

        АРГУМЕНТЫ:

        dictionary: dict
            Принимает словарь данных.
        key: str
            Принимает ключ для поиска значения в словаре.

        ВОЗВРАЩАЕТ:

        str | list | int | None
            В зависимости от условий, может возвращать строку, список, число.
        """
        if not isinstance(dictionary, dict):
            return None

        dict_value = dictionary.get(key)
        if dict_value is not None:
            return dict_value

        for nested_dict in dictionary.values():
            dict_value = self.__get_value(nested_dict, key)
            if dict_value is not None:
                return dict_value

        return None


class ReceiptParser:
    """
    Класс парсинга чека.

    В методах этого класса, все данные записываются в базу данных.

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

    def __init__(self, json_data):
        """Метод-конструктор инициализирующий аргумент json_data."""
        self.json_data = json_data
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
        products_list = self.parser.parse_json(
            self.json_data, constants.ITEMS_PRODUCT,
        )
        for product in products_list:
            product_name = self.parser.parse_json(
                product, constants.PRODUCT_NAME,
            )
            price = convert_number(
                self.parser.parse_json(
                    product, constants.PRICE,
                ),
            )
            quantity = self.parser.parse_json(
                product, constants.QUANTITY,
            )
            amount = convert_number(self.parser.parse_json(
                product, constants.AMOUNT,
            ))
            nds_type = self.parser.parse_json(
                product, constants.NDS_TYPE,
            )
            nds_sum = convert_number(self.parser.parse_json(
                product, constants.NDS_SUM,
            ))

            products = Product.objects.create(
                product_name=product_name,
                price=price,
                quantity=quantity,
                amount=amount,
                nds_type=nds_type,
                nds_sum=nds_sum,
            )
            self.product_list.append(products)
        self.receipt.product.set(self.product_list)

    def parse_customer(self) -> None:
        """
        Метод класса для парсинга продавца из JSON данных чека.

        Парсинг включает в себя название продавца, например: ООО "Пятерочка".
        Фактический адрес расположения магазина, в котором был распечатан чек.
        Название того магазина, где был распечатан чек.
        """
        name_seller = self.parser.parse_json(
            self.json_data, constants.NAME_SELLER,
        )
        retail_place_address = self.parser.parse_json(
            self.json_data, constants.RETAIL_PLACE_ADDRESS,
        )
        retail_place = self.parser.parse_json(
            self.json_data, constants.RETAIL_PLACE,
        )
        self.customer = Customer.objects.create(
            name_seller=name_seller,
            retail_place_address=retail_place_address,
            retail_place=retail_place,
        )

    def parse_receipt(self, chat_id: int) -> None:  # noqa: WPS210
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
        receipt_date = convert_date_time(self.parser.parse_json(
            self.json_data, constants.RECEIPT_DATE,
        ))
        number_receipt = self.parser.parse_json(
            self.json_data, constants.NUMBER_RECEIPT,
        )
        operation_type = self.parser.parse_json(
            self.json_data, constants.OPERATION_TYPE,
        )
        total_sum = convert_number(self.parser.parse_json(
            self.json_data, constants.TOTAL_SUM,
        ))

        if operation_type in {2, 3}:
            total_sum = -total_sum

        check_number_receipt = Receipt.objects.filter(
            number_receipt=number_receipt,
        ).first()

        if check_number_receipt:
            bot_admin.send_message(chat_id, 'Чек существует')
            return
        else:
            self.parse_customer()
            self.receipt = Receipt.objects.create(
                receipt_date=receipt_date,
                number_receipt=number_receipt,
                operation_type=operation_type,
                total_sum=total_sum,
                customer=self.customer,
            )
            self.parse_products()
            bot_admin.send_message(chat_id, 'Чек принят!')

    def parse(self, chat_id: int) -> None:
        """
        Метод отвечает за вызов метода `parse_receipt` по парсингу чека.

        В случае ошибки выбрасывает исключение и отправляет ошибку пользователю.

        :argument chat_id: ID пользователя, кому направлять сообщения.


        :raises: ValueError, KeyError, AttributeError, TypeError, IntegrityError

        """
        try:
            self.parse_receipt(chat_id)
        except (ValueError, KeyError) as value_key_error:
            logger.error(value_key_error)
        except (AttributeError, TypeError, IntegrityError) as complex_error:
            logger.error(complex_error)
        except Exception as error:
            logger.error(
                f'{error}Время возникновения исключения: '
                f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S}',
            )
