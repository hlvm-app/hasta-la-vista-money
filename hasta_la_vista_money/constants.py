from enum import Enum

from django.utils.translation import gettext_lazy as _


class ReceiptConstants(Enum):
    NAME_SELLER = 'user'
    RETAIL_PLACE_ADDRESS = 'retailPlaceAddress'
    RETAIL_PLACE = 'retailPlace'
    RECEIPT_DATE_TIME = 'dateTime'
    RECEIPT_DATE = 'date'
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
    RECEIPT_ALREADY_EXISTS = _('Такой чек уже существует в базе!')
    RECEIPT_CANNOT_BE_ADDED = _(
        'Чек не корректен, перепроверьте в приложении налоговой!',
    )


class Messages(Enum):
    SUCCESS_MESSAGE_LOGIN = _('Вы успешно авторизовались!')
    SUCCESS_MESSAGE_REGISTRATION = _('Регистрация прошла успешно!')
    ACCESS_DENIED = _(
        'У вас нет прав на просмотр данной страницы! Авторизуйтесь!',
    )
    SUCCESS_MESSAGE_CREATE_RECEIPT = _(
        'Чек был успешно добавлен в базу данных!',
    )


class HTTPStatus(Enum):
    SUCCESS_CODE = 200
    SERVER_ERROR = 500
    NOT_FOUND = 404


class ResponseText(Enum):
    SUCCESS_WEBHOOKS = _('Webhook processed successfully')
    WEBHOOKS_TELEGRAM = _('This page for Webhooks Telegram!')


class SessionCookie(Enum):
    SESSION_COOKIE_AGE = 1209600
