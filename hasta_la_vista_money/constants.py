import datetime
from enum import Enum


class ReceiptConstants(Enum):
    NAME_SELLER = 'user'
    RETAIL_PLACE_ADDRESS = 'retailPlaceAddress'
    RETAIL_PLACE = 'retailPlace'
    RECEIPT_DATE_TIME = 'dateTime'
    NUMBER_RECEIPT = 'fiscalDocumentNumber'
    NUMBER_RECEIPT_ID = 'documentId'
    OPERATION_TYPE = 'operationType'
    TOTAL_SUM = 'totalSum'
    PRODUCT_NAME = 'name'
    PRICE = 'price'
    QUANTITY = 'quantity'
    AMOUNT = 'sum'
    NDS_TYPE = 'nds'
    NDS_SUM = 'ndsSum'
    ITEMS_PRODUCT = 'items'
    RECEIPT_ALREADY_EXISTS = 'Такой чек уже существует в базе!'
    RECEIPT_CANNOT_BE_ADDED = (
        'Чек не корректен, перепроверьте в приложении налоговой!',
    )
    RECEIPT_BE_ADDED = 'Чек добавлен в базу данных!'
    RECEIPT_NOT_ACCEPTED = ''.join(
        (
            'Чек не прошёл валидацию!\n',
            'Вероятно он ещё не попал в базу данных налоговой!\n',
            'Обычно чек попадает в базу не позже суток.\n',
            'Попробуйте позже или внесите данные вручную на сайте.',
        ),
    )
    QR_CODE_NOT_CONSIDERED = ''.join(
        (
            'QR-код не считался, попробуйте ещё раз или ',
            'воспользуйтесь сторонним приложением ',
            'и передайте текст из QR-кода боту',
        ),
    )


class Messages(Enum):
    SUCCESS_MESSAGE_LOGIN = 'Вы успешно авторизовались!'
    SUCCESS_MESSAGE_REGISTRATION = 'Регистрация прошла успешно!'
    ACCESS_DENIED = (
        'У вас нет прав на просмотр данной страницы! Авторизуйтесь!',
    )
    SUCCESS_MESSAGE_CREATE_RECEIPT = (
        'Чек был успешно добавлен в базу данных!',
    )


class HTTPStatus(Enum):
    SUCCESS_CODE = 200
    SERVER_ERROR = 500
    NOT_FOUND = 404


class ResponseText(Enum):
    SUCCESS_WEBHOOKS = 'Webhook processed successfully'
    WEBHOOKS_TELEGRAM = 'This page for Webhooks Telegram!'


class SessionCookie(Enum):
    SESSION_COOKIE_AGE = 1209600


CURRENT_YEAR = datetime.date.today().year


class NumberMonthOfYear(Enum):
    NUMBER_FIRST_MONTH_YEAR = 1
    NUMBER_SECOND_MONTH_YEAR = 2
    NUMBER_THIRD_MONTH_YEAR = 3
    NUMBER_FOURTH_MONTH_YEAR = 4
    NUMBER_FIFTH_MONTH_YEAR = 5
    NUMBER_SIXTH_MONTH_YEAR = 6
    NUMBER_SEVENTH_MONTH_YEAR = 7
    NUMBER_EIGHTH_MONTH_YEAR = 8
    NUMBER_NINTH_MONTH_YEAR = 9
    NUMBER_TENTH_MONTH_YEAR = 10
    NUMBER_ELEVENTH_MONTH_YEAR = 11
    NUMBER_TWELFTH_MONTH_YEAR = 12


MONTH_NUMBERS = {  # noqa: WPS407
    'Январь': 1,
    'Февраль': 2,
    'Март': 3,
    'Апрель': 4,
    'Май': 5,
    'Июнь': 6,
    'Июль': 7,
    'Август': 8,
    'Сентябрь': 9,
    'Октябрь': 10,
    'Ноябрь': 11,
    'Декабрь': 12,
}

MONTH_NAMES = {  # noqa: WPS407
    1: 'Январь',
    2: 'Февраль',
    3: 'Март',
    4: 'Апрель',
    5: 'Май',
    6: 'Июнь',
    7: 'Июль',
    8: 'Август',
    9: 'Сентябрь',
    10: 'Октябрь',
    11: 'Ноябрь',
    12: 'Декабрь',
}
