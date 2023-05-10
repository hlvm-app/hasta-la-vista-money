from constantly import ValueConstant, Values


class ReceiptConstant(Values):
    NAME_SELLER = ValueConstant('user')
    RETAIL_PLACE_ADDRESS = ValueConstant('retailPlaceAddress')
    RETAIL_PLACE = ValueConstant('retailPlace')
    RECEIPT_DATE = ValueConstant('dateTime')
    NUMBER_RECEIPT = ValueConstant('fiscalDocumentNumber')
    OPERATION_TYPE = ValueConstant('operationType')
    TOTAL_SUM = ValueConstant('totalSum')
    PRODUCT_NAME = ValueConstant('name')
    PRICE = ValueConstant('price')
    QUANTITY = ValueConstant('quantity')
    AMOUNT = ValueConstant('sum')
    NDS_TYPE = ValueConstant('nds')
    NDS_SUM = ValueConstant('ndsSum')
    ITEMS_PRODUCT = ValueConstant('items')
