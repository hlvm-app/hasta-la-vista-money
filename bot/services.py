import datetime
import os

import requests
from dotenv import load_dotenv


# Выделяем дату из json
def convert_date_time(date_time):
    return f"{datetime.datetime.fromtimestamp(date_time):%Y-%m-%d %H:%M}"


def convert_price(price):
    return round(price / 100, 2)


class ParseJson:
    def __init__(self, json_data):
        self.json_data = json_data

    def _get_value(self, dictionary, key):
        if isinstance(dictionary, dict):
            for k, v in dictionary.items():
                if k == key:
                    return v
                elif isinstance(v, dict):
                    result = ParseJson._get_value(self, v, key)
                    if result is not None:
                        return result

        return None

    def parse_json(self, json_data: dict, key: str):
        result = ParseJson._get_value(self, json_data, key)
        return result


class ReceiptApiReceiver:
    def __init__(self) -> None:
        load_dotenv()
        self.__session_id = None
        self.host = 'irkkt-mobile.nalog.ru:8888'
        self.device_os = 'Android'
        self.client_version = '2.9.0'
        self.device_id = 'a5e1e72bf5b9966690e10f5ce03cd8e99e0b23dc4'
        self.accept = '*/*'
        self.user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) '\
                          'Gecko/20100101 Firefox/110.0'
        self.accept_language = 'ru-RU;q=1, en-US;q=0.9'
        self.set_session_id()

    def set_session_id(self) -> None:
        client_secret = [env for env in ['CLIENT_SECRET', 'INN', 'PASSWORD']
                         if os.getenv(env) is None]
        if client_secret:
            raise ValueError(f'OS environments not content '
                             f'{", ".join(client_secret)}')

        url = f'https://{self.host}/v2/mobile/users/lkfl/auth'
        payload = {
            'inn': os.getenv('INN'),
            'client_secret': os.getenv('CLIENT_SECRET'),
            'password': os.getenv('PASSWORD')
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

        response = requests.post(url, json=payload, headers=headers)
        self.__session_id = response.json()['sessionId']

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
            'sessionId': self.__session_id,
            'User-Agent': self.user_agent,
        }
        resp = requests.post(url, json=payload, headers=headers)
        return resp.json()["id"]

    def get_receipt(self, qr: str) -> dict:
        ticket_id = self._get_receipt_id(qr)
        url = f'https://{self.host}/v2/tickets/{ticket_id}'
        headers = {
            'Host': self.host,
            'sessionId': self.__session_id,
            'Device-OS': self.device_os,
            'clientVersion': self.client_version,
            'Device-Id': self.device_id,
            'Accept': self.accept,
            'User-Agent': self.user_agent,
            'Accept-Language': self.accept_language,
        }
        resp = requests.get(url, headers=headers)
        return resp.json()
