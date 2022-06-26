import json

from bot.services import convert_date_time, get_result_price, remove_json_file
from receipts.models import Receipt
from settings_bot import bot_admin


@bot_admin.message_handler(func=lambda message: message.document.mime_type ==
                                                'application/json',
                           content_types=['document'])
def get_receipt(message):
    try:
        file_info = bot_admin.get_file(message.document.file_id)
        file_downloaded = bot_admin.download_file(
            file_path=file_info.file_path)
        src = f'bot/receipts/{message.document.file_name}'
        with open(src, 'wb') as file:
            file.write(file_downloaded)

        with open(file.name, 'r') as json_file:
            json_data = json.load(json_file)
            date_time = convert_date_time(json_data["dateTime"])
            seller = json_data['user']
            total_sum = str(get_result_price(json_data["totalSum"]))
            information_products = []

            for item in json_data["items"]:
                name_product = item["name"]
                price = str(get_result_price(item["price"]))
                quantity = str(item["quantity"])
                amount = str(get_result_price(item["sum"]))
                list_product_information = [name_product, price, quantity,
                                            amount]
                information_products.append(list_product_information)

            Receipt.objects.get_or_create(
                receipt_date=date_time,
                name_seller=seller,
                product_information=information_products,
                total_sum=total_sum
            )
            bot_admin.send_message(message.chat.id, 'Чек принят!')
        remove_json_file(src)
    except Exception as error:
        bot_admin.send_message(message.chat.id, f'Чек не был добавлен!\n'
                                                f'Произошла ошибка!\n'
                                                f'{error}')


