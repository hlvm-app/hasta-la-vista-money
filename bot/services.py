import datetime


# Выделяем дату из json
def convert_date(date_time):
    return datetime.datetime.fromtimestamp(date_time).strftime("%Y.%m.%d")


# Выделяем время из json
def convert_time(date_time):
    return datetime.datetime.fromtimestamp(date_time).strftime("%H:%M:%S")


def get_result_price(price):
    return round(price / 100, 2)
