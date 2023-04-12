"""Модуль разбора json данных."""

import datetime
import types

from django.db import IntegrityError
from hasta_la_vista_money.bot.config_bot import bot_admin
from hasta_la_vista_money.bot.log_config import logger
from hasta_la_vista_money.bot.services import convert_date_time, convert_number
from hasta_la_vista_money.receipts.models import Customer, Product, Receipt

CONSTANT_RECEIPT = types.MappingProxyType(
    {
        'name_seller': 'user',
        'retail_place_address': 'retailPlaceAddress',
        'retail_place': 'retailPlace',
        'receipt_date': 'dateTime',
        'number_receipt': 'fiscalDocumentNumber',
        'operation_type': 'operationType',
        'total_sum': 'totalSum',
        'product_name': 'name',
        'price': 'price',
        'quantity': 'quantity',
        'amount': 'sum',
        'nds_type': 'nds',
        'nds_sum': 'ndsSum',
        'items': 'items',
    },
)


class JsonParser:
    """Универсальный класс разбора json данных."""

    def __init__(self, json_data):
        """
        Метод-конструктор инициализирующий аргумент json_data.

        :param json_data: Инициализация аргумента содержащий json данные.
        """
        self.json_data = json_data

    def parse_json(
        self, json_data: dict, key: str,
    ) -> list[dict] | int | str | None:
        """
        Метод разбора json данных.

        :param json_data: json данные.
        :type: dict
        :param key: Ключ для поиска в словаре.
        :type: str
        :return:
        :rtype: list[dict] | None
        """
        return JsonParser.__get_value(self, json_data, key)

    def __get_value(  # noqa: WPS112
        self, dictionary, key,
    ) -> str | list | int | None:
        """
        Приватный метод получения значений из словаря (json данных).

        :param dictionary: json данные - словарь.
        :type: dict
        :param key: Ключ для поиска в словаре.
        :type: str
        :return:
        :rtype: str | list | int | None
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
    """

    def __init__(self, json_data):
        """
        Метод-конструктор инициализирующий аргумента json_data.

        Также, определяются переменные класса:
        parser,
        customer,
        receipt,
        product_list
        :param json_data:
        :type: dict
        """
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

        :return: None
        """
        products_list = self.parser.parse_json(
            self.json_data, CONSTANT_RECEIPT.get('items'),
        )
        for product in products_list:
            product_name = self.parser.parse_json(
                product, CONSTANT_RECEIPT.get('product_name', None),
            )
            price = convert_number(
                self.parser.parse_json(
                    product, CONSTANT_RECEIPT.get('price', 0),
                ),
            )
            quantity = self.parser.parse_json(
                product, CONSTANT_RECEIPT.get('quantity', 0),
            )
            amount = convert_number(self.parser.parse_json(
                product, CONSTANT_RECEIPT.get('amount', 0),
            ))
            nds_type = self.parser.parse_json(
                product, CONSTANT_RECEIPT.get('nds_type', None),
            )
            nds_sum = convert_number(self.parser.parse_json(
                product, CONSTANT_RECEIPT.get('nds_sum', 0),
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
        r"""
        Метод класса для парсинга продавца из JSON данных чека.

        Парсинг включает в себя название продавца, например: ООО "Пятерочка".\n
        Фактический адрес расположения магазина, в котором был распечатан чек.\n
        Название того магазина, где был распечатан чек.

        :return: None
        """
        name_seller = self.parser.parse_json(
            self.json_data, CONSTANT_RECEIPT.get('name_seller', None),
        )
        retail_place_address = self.parser.parse_json(
            self.json_data, CONSTANT_RECEIPT.get('retail_place_address', None),
        )
        retail_place = self.parser.parse_json(
            self.json_data, CONSTANT_RECEIPT.get('retail_place', None),
        )
        self.customer = Customer.objects.create(
            name_seller=name_seller,
            retail_place_address=retail_place_address,
            retail_place=retail_place,
        )

    def parse_receipt(self, chat_id: int) -> None:  # noqa: WPS210
        r"""
        Метод класса для парсинга основной информации о чеке.

        Парсится дата чека, номер, тип операции(Приход, расход и пр.) и итоговая
        сумма.\n

        В методе также проверяется существование номера чека в базе данных,
        чтобы исключить дубли.\n
        По итогу, если чек существует или был добавлен, отправляется
        сообщение тому пользователю, кто попытался добавить чек.

        :param chat_id: ID пользователя, кому направлять сообщения.
        :type: int
        :return: None
        """
        receipt_date = convert_date_time(self.parser.parse_json(
            self.json_data, CONSTANT_RECEIPT.get('receipt_date', None),
        ))
        number_receipt = self.parser.parse_json(
            self.json_data, CONSTANT_RECEIPT.get('number_receipt', None),
        )
        operation_type = self.parser.parse_json(
            self.json_data, CONSTANT_RECEIPT.get('operation_type', None),
        )
        total_sum = convert_number(self.parser.parse_json(
            self.json_data, CONSTANT_RECEIPT.get('total_sum', 0),
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

    def parse(self, chat_id):
        """
        Метод отвечает за вызов метода по парсингу чека.

        В случае ошибки выбрасывает исключение.

        :param chat_id: ID пользователя, кому направлять сообщения.
        :type: int
        :return: None
        :raise: ValueError, KeyError, AttributeError, TypeError, IntegrityError

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
