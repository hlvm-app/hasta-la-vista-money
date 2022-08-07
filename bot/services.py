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
        return os.remove(os.path.join(path, file))


def parse_json_file(json_data):
    date_time = convert_date_time(json_data["dateTime"])
    seller = json_data['user']
    total_sum = str(get_result_price(json_data["totalSum"]))
    retail_place_address = json_data['retailPlaceAddress']
    operation_type = json_data['operationType']
    retail_place = json_data['retailPlace']
    information_products = []

    for item in json_data["items"]:
        name_product = item["name"]
        price = str(get_result_price(item["price"]))
        quantity = str(item["quantity"])
        amount = str(get_result_price(item["sum"]))
        payment_type = item['paymentType']
        product_type = item['productType']
        nds_type = item['nds']
        list_product_information = [name_product, price, quantity,
                                    amount, payment_type, product_type,
                                    nds_type]
        information_products.append(list_product_information)
    return date_time, seller, total_sum, retail_place_address, \
        operation_type, retail_place, information_products
