import json
import os

import requests
from dotenv import load_dotenv
from hasta_la_vista_money.bot.log_config import logger


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
        self.user_agent = ''.join(
            (
                'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) ',
                'Gecko/20100101 Firefox/110.0',
            ),
        )
        self.accept_language = 'ru-RU;q=1, en-US;q=0.9'
        self.session_id()

    def session_id(self) -> None:
        """
        Получает идентификатор сессии в сервисе налоговой службы РФ.

        Если не удалось получить идентификатор, вызывает исключение ValueError.

        Raises:
            ValueError: Ошибка переданного значения
        """
        try:
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

            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=10,
            )
            self._session_id = response.json()['sessionId']
        except (
            requests.exceptions.ConnectionError,
            json.decoder.JSONDecodeError,
            requests.exceptions.ReadTimeout,
        ):
            logger.error('Недоступен сервис авторизации. Попробуйте позже!')

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
