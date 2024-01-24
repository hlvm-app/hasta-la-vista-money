import datetime
from typing import Any, Optional, Union

from hasta_la_vista_money.account.models import Account
from hasta_la_vista_money.bot.log_config import logger
from hasta_la_vista_money.users.models import TelegramUser


# Выделяем дату из json
def convert_date_time(
    date_time: list[dict[Any, Any]] | int | str | None,
) -> Optional[str]:
    """
    Конвертация unix time числа в читабельное представление даты и времени.

    :param date_time: Unix timestamp (Количество секунд от
                    1970-01-01 00:00:00 UTC)
    :type date_time: Union[str, int]
    :return: Строка с читабельным представлением даты и времени
    :rtype: str
    :raise: TypeError: Если аргумент не является целым числом

    """
    try:
        if date_time is None:
            return None
        if isinstance(date_time, str):
            dt = datetime.datetime.strptime(
                date_time,
                '%Y-%m-%dT%H:%M:%S',
            )
            return dt.strftime('%Y-%m-%d %H:%M')
        dt = datetime.datetime.fromtimestamp(int(date_time))
        return f'{dt:%Y-%m-%d %H:%M}'
    except TypeError as error:
        logger.error(f'Из JSON пришло неправильное число у даты чека: {error}')


def convert_number(
    number: list[dict[Any, Any]] | int | str | None,
) -> Union[int, float]:
    """
    Конвертация числа полученного из JSON в число с плавающей точкой.

    Служит для того, чтобы число преобразовать в рубли и копейки.

    :param number: Целое число получаемое из JSON ключей с ценой, суммой товаров
                   и НДС + итоговая сумма чека.
    :type number: int
    :return: Возвращает число с плавающей точкой.
    :rtype: float
    """
    return round(number / 100, 2) if number else 0


def get_telegram_user(message):
    """
    Функция получения о наличии телеграм пользователя в базе данных.

    :param message:
    :return:
    """
    return TelegramUser.objects.filter(
        telegram_id=message.from_user.id,
    ).first()


def check_account_exist(user):
    """
    Проверка существования счёта.

    :param user:
    :return:
    """
    return Account.objects.filter(user=user).first()
