def respond(bot, chat_id, message):
    return bot.send_message(chat_id=chat_id, **message)
