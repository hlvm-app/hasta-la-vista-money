from hasta_la_vista_money.bot.bot_handler import check_telegram_user
from hasta_la_vista_money.bot.config_bot import bot_admin
from hasta_la_vista_money.constants import TelegramMessage
from hasta_la_vista_money.users.models import TelegramUser, User


@bot_admin.message_handler(commands=['auth'])
def handle_start(message):
    """
    Обработка команды /auth.

    :param message:
    :return:
    """
    bot_admin.send_message(
        message.chat.id,
        TelegramMessage.REQUIRED_AUTHORIZATION.value,
    )
    bot_admin.register_next_step_handler(message, handle_auth)


def handle_auth(message):
    """
    Обработка логина и пароля от сайта для авторизации в боте.

    :param message:
    :return:
    """
    auth_data = message.text.split(':')
    if len(auth_data) != 2:
        bot_admin.reply_to(message, TelegramMessage.INCORRECT_FORMAT.value)
        return

    username, password = map(str, auth_data)
    user = User.objects.filter(username=username).first()

    if user and user.check_password(password):
        check_existing_telegram_user(message, user)
    else:
        bot_admin.reply_to(
            message,
            TelegramMessage.INVALID_USERNAME_PASSWORD.value,
        )
        bot_admin.delete_message(message.from_user.id, message.message_id)


def check_existing_telegram_user(message, user):
    """
    Проверка существования телеграм пользователя в базе данных.

    Если пользователь существует, то отправляется сообщение пользователю
    о том, что пользователь уже авторизован. В ином случае, создает запись
    в базе данных.

    :param message:
    :param user:
    :return:
    """
    if check_telegram_user(message):
        authenticated_user(message)
    else:
        create_telegram_user(message, user)


def authenticated_user(message):
    """
    Функция для проверки, авторизован ли пользователь в боте.

    :param message:
    :return:
    """
    if check_telegram_user(message):
        bot_admin.send_message(
            message.chat.id,
            TelegramMessage.ALREADY_LOGGING_LINK_ACCOUNT.value,
        )
        bot_admin.delete_message(message.from_user.id, message.message_id)
    else:
        bot_admin.send_message(
            message.chat.id,
            TelegramMessage.ALREADY_LINK_ANOTHER_ACCOUNT.value,
        )
        bot_admin.delete_message(message.from_user.id, message.message_id)


def create_telegram_user(message, user):
    """
    Создание записи в базе данных с данными о телеграм пользователе.

    :param message:
    :param telegram_username:
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
        TelegramMessage.AUTHORIZATION_SUCCESSFUL.value,
    )
    bot_admin.delete_message(message.from_user.id, message.message_id)