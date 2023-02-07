import datetime
import os


# Выделяем дату из json
def convert_date_time(date_time):
    return f"{datetime.datetime.fromtimestamp(date_time):%Y-%m-%d %H:%M}"


def convert_price(price):
    return round(price / 100, 2)


def parse_json_file(json_data):
    date_time = convert_date_time(json_data.get('dateTime', 'Нет данных'))
    seller = json_data.get('user', 'Нет данных')
    total_sum = convert_price(json_data.get('totalSum', 'Нет данных'))
    retail_place_address = json_data.get('retailPlaceAddress', 'Нет данных')
    operation_type = json_data.get('operationType', 'Нет данных')
    retail_place = json_data.get('retailPlace', 'Нет данных')

    return date_time, seller, total_sum, retail_place_address, \
        operation_type, retail_place
