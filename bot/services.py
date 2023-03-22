import datetime
import os

import requests
from dotenv import load_dotenv


# Выделяем дату из json
def convert_date_time(date_time):
    return f'{datetime.datetime.fromtimestamp(date_time):%Y-%m-%d %H:%M}'


def convert_price(price):
    if price is None:
        return None
    return round(price / 100, 2)


class ReceiptApiReceiver:
    def __init__(self) -> None:
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

    def session_id(self):
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

    def get_receipt(self, qr: str) -> dict:
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
