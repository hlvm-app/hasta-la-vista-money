from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def markup():
    keyboard_markup = InlineKeyboardMarkup(row_width=3)
    btn1 = InlineKeyboardButton("Дата чека", callback_data='date')
    btn2 = InlineKeyboardButton("Имя продавца", callback_data='seller')
    btn3 = InlineKeyboardButton("Итоговая сумма чека", callback_data='total')
    btn4 = InlineKeyboardButton("Информация о товарах в чеке",
                                callback_data='products')
    result_btn = InlineKeyboardButton("Добавить чек в базу данных",
                                      callback_data='result')
    keyboard_markup.add(btn1, btn2, btn3, btn4, result_btn)

    return keyboard_markup
