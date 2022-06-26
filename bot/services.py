import datetime
import os


# Выделяем дату из json
def convert_date_time(date_time):
    return datetime.datetime.fromtimestamp(date_time).strftime("%Y-%m-%d "
                                                               "%H:%M")


def get_result_price(price):
    return round(price / 100, 2)


def remove_json_file(path):
    list_dir = os.listdir(path)
    for file in list_dir:
        os.remove(f'receipts/{file}')
