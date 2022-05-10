import datetime


# Выделяем дату из json
def convert_date_time(date_time):
    return datetime.datetime.fromtimestamp(date_time).strftime("%d-%m-%Y "
                                                               "%H:%M:%S")


def get_result_price(price):
    return round(price / 100, 2)
