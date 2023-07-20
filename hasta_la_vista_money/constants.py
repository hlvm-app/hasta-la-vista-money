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


class MessageOnSite(Enum):
    SUCCESS_MESSAGE_LOGIN = 'Вы успешно авторизовались!'
    SUCCESS_MESSAGE_REGISTRATION = 'Регистрация прошла успешно!'
    SUCCESS_MESSAGE_CREATE_RECEIPT = ''.join(
        'Чек успешно добавлен в базу данных!',
    )
    ANOTHER_ACCRUAL_ACCOUNT = ' '.join((
        'Нельзя выбирать одинаковые счета для перевода.',
    ))
    SUCCESS_MESSAGE_CHANGED_ACCOUNT = 'Счёт успешно изменён!'
    SUCCESS_MESSAGE_CHANGED_PROFILE = 'Профиль успешно обновлён!'
    SUCCESS_MESSAGE_CHANGED_PASSWORD = 'Новый пароль успешно установлен!'  # noqa: E501 S105
    SUCCESS_MESSAGE_LOGOUT = 'Вы успешно вышли из своей учётной записи!'
    HELP_TEXT_PASSWORD = ''.join(
        (
            'Пароли хранятся в зашифрованном виде, ',
            'поэтому нет возможности посмотреть ваш пароль, ',
            'но вы можете установить новый на вкладке "Установить пароль"',
        ),
    )
    SUCCESS_CATEGORY_ADDED = 'Категория добавлена!'
    SUCCESS_INCOME_ADDED = 'Операция дохода успешно добавлена!'
    SUCCESS_INCOME_DELETED = 'Операция дохода успешно удалена!'
    SUCCESS_CATEGORY_INCOME_DELETED = 'Категория дохода успешно удалена!'
    ACCESS_DENIED_DELETE_CATEGORY_INCOME = ''.join(
        (
            'Категория не может быть удалена, ',
            'так как связана с одним из пунктом дохода',
        ),
    )
    SUCCESS_MESSAGE_TRANSFER_MONEY = 'Средства успешно переведены'
    SUCCESS_MESSAGE_INSUFFICIENT_FUNDS = 'Недостаточно средств'


class TelegramMessage(Enum):
    SAFE_LOGIN_PASSWORD = ''.join(
        (
            'Ваш логин и пароль был удалены для обеспечения сохранности ',
            'конфиденциальных данных!',
        ),
    )
    ALREADY_LOGGING_LINK_ACCOUNT = ''.join(
        (
            'Вы уже авторизованы и связаны с этим аккаунтом.\n',
            SAFE_LOGIN_PASSWORD,
        ),
    )

    ALREADY_LINK_ANOTHER_ACCOUNT = ''.join(
        (
            'Ваш аккаунт уже связан с другим Telegram аккаунтом.\n',
            SAFE_LOGIN_PASSWORD,
        ),
    )

    AUTHORIZATION_SUCCESSFUL = ''.join(
        (
            'Авторизация прошла успешно. Вы привязаны к своему аккаунту.\n',
            SAFE_LOGIN_PASSWORD,
        ),
    )

    INVALID_USERNAME_PASSWORD = ''.join(
        (
            'Неверный логин или пароль. Попробуйте ещё раз.\n',
            SAFE_LOGIN_PASSWORD,
        ),
    )

    INCORRECT_FORMAT = ''.join(
        (
            'Некорректный формат. Повторите ввод логина и пароля.\n',
            SAFE_LOGIN_PASSWORD,
        ),
    )

    REQUIRED_AUTHORIZATION = ''.join(
        (
            'Требуется авторизация.\n',
            'Введите логин и пароль в формате: логин:пароль',
        ),
    )

    ACCEPTED_FORMAT_JSON = (
        'Принимаются файлы JSON, текст по формату и фотографии QR-кодов',
    )

    NOT_CREATE_ACCOUNT = 'Не создан счёт! Сначала создайте счёт на сайте!'
    ERROR_DATABASE_RECORD = 'Ошибка записи в базу данных!'
    ALREADY_LOGGED = 'Вы уже авторизованы!'


class HTTPStatus(Enum):
    SUCCESS_CODE = 200
    SERVER_ERROR = 500
    NOT_FOUND = 404
    REDIRECTS = 302


class NumericParameter(Enum):
    TWO = 2
    TEN = 10
    TWENTY = 10
    THIRTY = 30
    FORTY = 40
    FIFTY = 50
    SIXTY = 60
    SEVENTY = 70
    EIGHTY = 80
    NINTY = 90
    ONE_HUNDRED = 100
    ONE_HUNDRED_FIFTY = 150
    TWO_HUNDRED = 200
    TWO_HUNDRED_FIFTY = 250
    DAY_MINUS_HOUR = 23
    MINUTE_MINUS_ONE = 59
    SECOND_MINUS_ONE = 59
    TODAY_MINUS_FIVE_YEARS = 23


class ResponseText(Enum):
    SUCCESS_WEBHOOKS = 'Webhook processed successfully'
    WEBHOOKS_TELEGRAM = 'This page for Webhooks Telegram!'


class SessionCookie(Enum):
    SESSION_COOKIE_AGE = 1209600


TODAY = datetime.datetime.today()
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


class TemplateHTMLView(Enum):
    INCOME_TEMPLATE = 'income/income.html'
    EXPENSE_TEMPLATE = 'expense/expense.html'
    RECEIPT_TEMPLATE = 'receipts/receipts.html'


class SuccessUrlView(Enum):
    INCOME_URL = 'income:list'
    EXPENSE_URL = 'expense:list'
    RECEIPT_URL = 'receipts:list'
