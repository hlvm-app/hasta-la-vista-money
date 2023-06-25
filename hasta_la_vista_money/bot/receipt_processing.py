import datetime
import decimal
import json
import os

import requests
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv
from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.bot.config_bot import bot_admin
from hasta_la_vista_money.bot.json_parse import JsonParser
from hasta_la_vista_money.bot.log_config import logger
from hasta_la_vista_money.bot.services import convert_date_time, convert_number
from hasta_la_vista_money.constants import ReceiptConstants, TelegramMessage
from hasta_la_vista_money.receipts.models import Customer, Product, Receipt


class ReceiptApiReceiver:
    """
    Класс для получения информации о чеке из базы налоговой службы РФ.

    АТРИБУТЫ:

    _session_id: str
        Идентификатор сессии, полученный при авторизации в сервисе.
    host: str
        URL-адрес сервиса.
    device_os: str
        Операционная система устройства.
    client_version: str
        Версия приложения клиента.
    device_id: str
        Идентификатор устройства.
    accept: str
        Строка с типом и версией принимаемого контента.
    user_agent: str
        User-Agent HTTP заголовка.
    accept_language: str
        Языковые предпочтения клиента для HTTP заголовка Accept-Language.

    МЕТОДЫ:

    session_id() -> None
        Получает идентификатор сессии в сервисе налоговой службы РФ.
        Внутренний метод, вызывается при создании экземпляра класса.
        Если не удалось получить идентификатор, вызывает исключение ValueError.

    get_receipt(qr: str) -> dict
        Получает информацию о чеке по QR-коду.
        Если не удалось получить информацию, записывает сообщение об ошибке в
        лог.

    _get_receipt_id(qr: str) -> str
        Получает идентификатор чека по QR-коду.
        Внутренний метод, используется в методе get_receipt().
    """

    def __init__(self) -> None:
        """
        Конструктор класса.

        Выполняет авторизацию в сервисе при создании экземпляра класса.

        """
        load_dotenv()
        self._session_id = None
        self.host = 'irkkt-mobile.nalog.ru:8888'
        self.device_os = 'Android'
        self.client_version = '2.9.0'
        self.device_id = 'a5e1e72bf5b9966690e10f5ce03cd8e99e0b23dc4'
        self.accept = '*/*'
        self.user_agent = (
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) '
            'Gecko/20100101 Firefox/110.0'
        )
        self.accept_language = 'ru-RU;q=1, en-US;q=0.9'
        self.session_id()

    def session_id(self) -> None:
        """
        Получает идентификатор сессии в сервисе налоговой службы РФ.

        Если не удалось получить идентификатор, вызывает исключение ValueError.

        """
        client_secret = [
            env
            for env in ('CLIENT_SECRET', 'INN', 'PASSWORD')
            if os.getenv(env) is None
        ]
        if client_secret:
            raise ValueError(
                f'OS environments not content {", ".join(client_secret)}',
            )

        url = f'https://{self.host}/v2/mobile/users/lkfl/auth'
        payload = {
            'inn': os.getenv('INN'),
            'client_secret': os.getenv('CLIENT_SECRET'),
            'password': os.getenv('PASSWORD'),
        }
        headers = {
            'Host': self.host,
            'Accept': self.accept,
            'Device-OS': self.device_os,
            'Device-Id': self.device_id,
            'clientVersion': self.client_version,
            'Accept-Language': self.accept_language,
            'User-Agent': self.user_agent,
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        self._session_id = response.json()['sessionId']

    def get_receipt(self, qr: str) -> dict | None:
        """
        Получает информацию о чеке по QR-коду.

        АРГУМЕНТЫ:

        qr: str
            QR-код, содержащий информацию о чеке.

        ВОЗВРАЩАЕТ:

        dict
            Словарь с информацией о чеке.

        Если не удалось получить информацию, записывает сообщение об ошибке в
        лог.
        """
        try:
            ticket_id = self._get_receipt_id(qr)
            url = f'https://{self.host}/v2/tickets/{ticket_id}'
            headers = {
                'Host': self.host,
                'sessionId': self._session_id,
                'Device-OS': self.device_os,
                'clientVersion': self.client_version,
                'Device-Id': self.device_id,
                'Accept': self.accept,
                'User-Agent': self.user_agent,
                'Accept-Language': self.accept_language,
            }

            resp = requests.get(url, headers=headers, timeout=10)
            return resp.json()
        except json.decoder.JSONDecodeError as json_error:
            logger.error(
                f'Ошибка обработки json: {json_error}\n'
                f'Время возникновения исключения: '
                f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S}',
            )

    def _get_receipt_id(self, qr: str) -> str:
        """
        Получает идентификатор чека по QR-коду.

        АРГУМЕНТЫ:

        qr: str
            QR-код, содержащий информацию о чеке.

        ВОЗВРАЩАЕТ:

        str
            Идентификатор чека.
        """
        url = f'https://{self.host}/v2/ticket'
        payload = {'qr': qr}
        headers = {
            'Host': self.host,
            'Accept': self.accept,
            'Device-OS': self.device_os,
            'Device-Id': self.device_id,
            'clientVersion': self.client_version,
            'Accept-Language': self.accept_language,
            'sessionId': self._session_id,
            'User-Agent': self.user_agent,
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        return resp.json()['id']


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
