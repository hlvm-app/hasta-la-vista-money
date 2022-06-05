def respond(bot, chat_id, message):
    return bot.send_message(chat_id=chat_id, **message)


def receipt_adding_accepted(bot, chat_id, message):
    return bot.send_message(chat_id=chat_id, **message)
