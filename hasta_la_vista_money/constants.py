from django.utils.translation import gettext_lazy as _
from enum import Enum


class ReceiptConstant(Enum):
    NAME_SELLER = 'user'
    RETAIL_PLACE_ADDRESS = 'retailPlaceAddress'
    RETAIL_PLACE = 'retailPlace'
    RECEIPT_DATE = 'dateTime'
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


class Messages(Enum):
    SUCCESS_MESSAGE_LOGIN = _('Вы успешно авторизовались')
    SUCCESS_MESSAGE_REGISTRATION = _('Регистрация прошла успешно!')
