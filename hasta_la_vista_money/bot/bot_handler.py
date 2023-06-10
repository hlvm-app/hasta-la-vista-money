from hasta_la_vista_money.bot.config_bot import bot_admin
from hasta_la_vista_money.bot.receipt_parser_json import handle_receipt_json
from hasta_la_vista_money.bot.receipt_parser_text import handle_receipt_text
from hasta_la_vista_money.bot.receipt_parser_text_qrcode import (
    handle_receipt_text_qrcode,
)
from hasta_la_vista_money.constants import TelegramMessage
from hasta_la_vista_money.users.models import Account, TelegramUser, User


@bot_admin.message_handler(commands=['auth'])
def handle_start(message):
    bot_admin.send_message(
        message.chat.id, TelegramMessage.REQUIRED_AUTHORIZATION.value,
    )
    bot_admin.register_next_step_handler(message, handle_auth)


def handle_auth(message):
    auth_data = message.text.split(':')
    if len(auth_data) == 2:
        username = auth_data[0].strip()
        password = auth_data[1].strip()
        user = User.objects.filter(username=username).first()
        telegram_username = message.from_user.username

        if user and user.check_password(password):
            existing_telegram_user = TelegramUser.objects.filter(
                user=user,
            ).first()
            if existing_telegram_user:
                if existing_telegram_user.telegram_id == message.from_user.id:
                    bot_admin.reply_to(
                        message,
                        TelegramMessage.ALREADY_LOGGING_LINK_ACCOUNT.value,
                    )
                else:
                    bot_admin.reply_to(
                        message,
                        TelegramMessage.ALREADY_LINK_ANOTHER_ACCOUNT.value,
                    )
            else:
                TelegramUser.objects.create(
                    user=user,
                    username=telegram_username,
                    telegram_id=message.from_user.id,
                )
                bot_admin.reply_to(
                    message, TelegramMessage.AUTHORIZATION_SUCCESSFUL.value,
                )
        else:
            bot_admin.reply_to(
                message, TelegramMessage.INVALID_USERNAME_PASSWORD.value,
            )
    else:
        bot_admin.reply_to(message, TelegramMessage.INCORRECT_FORMAT.value)


@bot_admin.message_handler(content_types=['text', 'document', 'photo'])
def handle_receipt(message):
    telegram_user_id = message.from_user.id

    telegram_user = TelegramUser.objects.filter(
        telegram_id=telegram_user_id
    ).first()

    if telegram_user:
        user = telegram_user.user
        account = Account.objects.filter(user=telegram_user.user).first()

        if message.content_type == 'text':
            handle_receipt_text(message, bot_admin, user, account)
        elif message.content_type == 'photo':
            handle_receipt_text_qrcode(message, bot_admin, user, account)
        elif message.content_type == 'document':
            handle_receipt_json(message, bot_admin, user, account)
        else:
            bot_admin.send_message(
                message.chat.id,
                TelegramMessage.ACCEPTED_FORMAT_JSON.value,
            )
