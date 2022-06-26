from settings_bot import bot_admin
from markup import markup
from receipts.models import Receipt


@bot_admin.message_handler(commands=['add'])
def add_receipt(message):
    text = message.text
    if text == '/add':
        bot_admin.send_message(message.chat.id, 'Выберите действие:',
                               reply_markup=markup())


result = []


@bot_admin.callback_query_handler(func=lambda call: True)
def callback(call):
    data = call.data
    message = call.message
    if data == 'date':
        bot_admin.send_message(message.chat.id, 'Введи дату')
        bot_admin.register_next_step_handler(message, get_receipt_date)
    if data == 'seller':
        bot_admin.send_message(message.chat.id, 'Введи имя продавца')
        bot_admin.register_next_step_handler(message, get_receipt_seller)
    if data == 'total':
        bot_admin.send_message(message.chat.id, 'Введи итоговую сумму чека')
        bot_admin.register_next_step_handler(message, get_receipt_total)
    if data == 'products':
        bot_admin.send_message(message.chat.id, 'Введи информацию о продуктах')
        bot_admin.register_next_step_handler(message, get_receipt_products)
    if data == 'result':
        bot_admin.send_message(message.chat.id,
                               'Чек будет добавлен в базу данных!')
        add_result_db(message)


def get_receipt_date(message):
    date = message.text
    result.append(date)


def get_receipt_seller(message):
    seller = message.text
    result.append(seller)


def get_receipt_total(message):
    total = message.text
    result.append(total)


def get_receipt_products(message):
    info = message.text
    result_info = info.split(';', maxsplit=-1)
    result.append(result_info)


def add_result_db(message):
    list2 = []
    for item in result[3]:
        list2.append(item.split(','))
    Receipt.objects.create(
        receipt_date=result[0],
        name_seller=result[1],
        total_sum=result[2],
        product_information=list2
    )
    bot_admin.send_message(message.chat.id, 'Чек добавлен!')
