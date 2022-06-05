import json
from telegram import Update
from telegram.ext import CallbackContext

import bot.views
from bot import helpers
from receipts.models import Receipt
from bot.services import convert_date_time, get_result_price


def get_receipt(update: Update, context: CallbackContext):
    data = update.message.document.get_file().download(
        custom_path='bot/receipts/receipt.json'
    )
    with open(data, 'r', encoding='UTF-8') as file_data:
        json_data = json.load(file_data)

        date_time = convert_date_time(json_data["dateTime"])
        seller = json_data['user']
        total_sum = str(get_result_price(json_data["totalSum"]))
        information_products = []

        for item in json_data["items"]:
            name_product = item["name"]
            price = str(get_result_price(item["price"]))
            quantity = str(item["quantity"])
            amount = str(get_result_price(item["sum"]))
            list_product_information = [name_product, price, quantity, amount]
            information_products.append(list_product_information)

        Receipt.objects.get_or_create(
            receipt_date=date_time,
            name_seller=seller,
            product_information=information_products,
            total_sum=total_sum
        )

    helpers.respond(context.bot, update.effective_chat.id,
                    bot.views.receipt_accepted())
