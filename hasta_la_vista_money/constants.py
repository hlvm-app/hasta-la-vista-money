from enum import Enum


class ReceiptConstants(Enum):
    NAME_SELLER = 'user'
    RETAIL_PLACE_ADDRESS = 'retailPlaceAddress'
    RETAIL_PLACE = 'retailPlace'
    RECEIPT_DATE_TIME = 'dateTime'
    NUMBER_RECEIPT = 'fiscalDocumentNumber'
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
