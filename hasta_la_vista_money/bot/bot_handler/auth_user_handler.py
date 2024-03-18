from hasta_la_vista_money import constants
from hasta_la_vista_money.bot.config_bot.config_bot import bot_admin
from hasta_la_vista_money.users.models import TelegramUser, CustomUser


def handle_auth(message):
    """
    Обработка логина и пароля от сайта для авторизации в боте.

    :param message:
    :return:
    """
    auth_data = message.text.split(':')
    if len(auth_data) != 2:
        bot_admin.reply_to(message, constants.INCORRECT_FORMAT)
        return

    username, password = map(str, auth_data)
    user = CustomUser.objects.filter(username=username).first()

    if user and user.check_password(password):
        create_telegram_user(message, user)
    else:
        bot_admin.reply_to(
            message,
            constants.INVALID_USERNAME_PASSWORD,
        )
        bot_admin.delete_message(message.from_user.id, message.message_id)


def create_telegram_user(message, user):
    """
    Создание записи в базе данных с данными о телеграм пользователе.

    :param message:
    :param user:
    :return:
    """
    TelegramUser.objects.create(
        user=user,
        username=message.from_user.username,
        telegram_id=message.from_user.id,
    )
    bot_admin.reply_to(
        message,
        constants.AUTHORIZATION_SUCCESSFUL,
    )
    bot_admin.delete_message(message.from_user.id, message.message_id)
