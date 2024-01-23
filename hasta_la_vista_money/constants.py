import datetime
from typing import Final

# Константы для парсинга json чека
NAME_SELLER: Final[str] = 'user'
RETAIL_PLACE_ADDRESS: Final[str] = 'retailPlaceAddress'
RETAIL_PLACE: Final[str] = 'retailPlace'
RECEIPT_DATE_TIME: Final[str] = 'dateTime'
NUMBER_RECEIPT: Final[str] = 'fiscalDocumentNumber'
NUMBER_RECEIPT_ID: Final[str] = 'documentId'
OPERATION_TYPE: Final[str] = 'operationType'
TOTAL_SUM: Final[str] = 'totalSum'
PRODUCT_NAME: Final[str] = 'name'
PRICE: Final[str] = 'price'
QUANTITY: Final[str] = 'quantity'
AMOUNT: Final[str] = 'sum'
NDS_TYPE: Final[str] = 'nds'
NDS_SUM: Final[str] = 'ndsSum'
NDS10: Final[str] = 'nds10'
NDS20: Final[str] = 'nds18'
ITEMS_PRODUCT: Final[str] = 'items'

# Константы строк для парсинга чека
RECEIPT_ALREADY_EXISTS: Final[str] = 'Такой чек уже существует!'
RECEIPT_BE_ADDED: Final[str] = 'Чек успешно добавлен!'
RECEIPT_CANNOT_BE_ADDED: Final[str] = ''.join(
    'Чек не корректен, перепроверьте в приложении налоговой!',
)
RECEIPT_NOT_ACCEPTED: Final[str] = ''.join(
    (
        'Чек не прошёл валидацию!\n',
        'Вероятно он ещё не попал в базу данных налоговой!\n',
        'Обычно чек попадает в базу не позже суток.\n',
        'Попробуйте позже или внесите данные вручную на сайте.',
    ),
)
QR_CODE_NOT_CONSIDERED: Final[str] = ''.join(
    (
        'QR-код не считался, попробуйте ещё раз или ',
        'воспользуйтесь сторонним приложением ',
        'и передайте текст из QR-кода боту',
    ),
)

# Сообщения для сайта
SUCCESS_MESSAGE_LOGIN: Final[str] = 'Вы успешно авторизовались!'
SUCCESS_MESSAGE_REGISTRATION: Final[str] = 'Регистрация прошла успешно!'
SUCCESS_MESSAGE_CREATE_RECEIPT: Final[str] = ''.join(
    'Чек успешно добавлен!',
)
SUCCESS_MESSAGE_CREATE_CUSTOMER: Final[str] = ''.join(
    'Новый продавец успешно добавлен!',
)
ANOTHER_ACCRUAL_ACCOUNT: Final[str] = ' '.join(
    'Нельзя выбирать одинаковые счета для перевода.',
)
SUCCESS_MESSAGE_ADDED_ACCOUNT: Final[str] = 'Счёт успешно создан!'
SUCCESS_MESSAGE_CHANGED_ACCOUNT: Final[str] = 'Счёт успешно изменён!'
SUCCESS_MESSAGE_DELETE_ACCOUNT: Final[str] = 'Счёт успешно удалён!'
UNSUCCESSFULLY_MESSAGE_DELETE_ACCOUNT: Final[str] = 'Счёт успешно удалён!'
SUCCESS_MESSAGE_CHANGED_PROFILE: Final[str] = 'Профиль успешно обновлён!'
SUCCESS_MESSAGE_CHANGED_PASSWORD: Final[str] = ''.join(
    'Новый пароль успешно установлен!',
)
SUCCESS_MESSAGE_LOGOUT: Final[str] = 'Вы успешно вышли из своей учётной записи!'
HELP_TEXT_PASSWORD: Final[str] = ''.join(
    (
        'Пароли хранятся в зашифрованном виде, ',
        'поэтому нет возможности посмотреть ваш пароль, ',
        'но вы можете поменять его на новый перейдя на вкладку<br>',
        '"Изменить пароль"',
    ),
)
HELP_TEXT_FORGOT_PASSWORD: Final[str] = ''.join(
    (
        'Укажите логин, который указывали при регистрации.<br>',
        'Ссылка для восстановления пароля будет выслана в чат с ботом.<br>',
        'После нажатия на кнопку ниже, ',
        'произойдёт переадресация в телеграм.',
    ),
)
SUCCESS_CATEGORY_ADDED: Final[str] = 'Категория добавлена!'
SUCCESS_EXPENSE_ADDED: Final[str] = 'Операция расхода успешно добавлена!'
SUCCESS_INCOME_ADDED: Final[str] = 'Операция дохода успешно добавлена!'
SUCCESS_INCOME_UPDATE: Final[str] = 'Операция дохода успешно обновлена!'
SUCCESS_EXPENSE_UPDATE: Final[str] = 'Операция расхода успешно обновлена!'
SUCCESS_EXPENSE_DELETED: Final[str] = 'Операция расхода успешно удалена!'
SUCCESS_INCOME_DELETED: Final[str] = 'Операция дохода успешно удалена!'
SUCCESS_CATEGORY_DELETED: Final[str] = 'Категория успешно удалена!'
ACCESS_DENIED_DELETE_CATEGORY: Final[str] = ''.join(
    (
        'Категория не может быть удалена, ',
        'так как связана с доходом или расходом',
    ),
)
SUCCESS_MESSAGE_TRANSFER_MONEY: Final[str] = 'Средства успешно переведены'
SUCCESS_MESSAGE_INSUFFICIENT_FUNDS: Final[str] = 'Недостаточно средств'
SUCCESS_MESSAGE_LOAN_CREATE: Final[str] = 'Кредит успешно добавлен'
SUCCESS_MESSAGE_LOAN_DELETE: Final[str] = 'Кредит успешно удалён'
SUCCESS_MESSAGE_PAYMENT_MAKE: Final[str] = 'Платеж успешно внесён'


# Сообщения для телеграма
SAFE_LOGIN_PASSWORD: Final[str] = ''.join(
    (
        'Ваш логин и пароль был удалены для обеспечения сохранности ',
        'конфиденциальных данных!',
    ),
)
ALREADY_LOGGING_LINK_ACCOUNT: Final[str] = ''.join(
    (
        'Вы уже авторизованы и связаны с этим аккаунтом.\n',
        SAFE_LOGIN_PASSWORD,
    ),
)

ALREADY_LINK_ANOTHER_ACCOUNT: Final[str] = ''.join(
    (
        'Ваш аккаунт уже связан с другим Telegram аккаунтом.\n',
        SAFE_LOGIN_PASSWORD,
    ),
)

AUTHORIZATION_SUCCESSFUL: Final[str] = ''.join(
    (
        'Авторизация прошла успешно. Вы привязаны к своему аккаунту.\n',
        SAFE_LOGIN_PASSWORD,
    ),
)

INVALID_USERNAME_PASSWORD: Final[str] = ''.join(
    (
        'Неверный логин или пароль. Попробуйте ещё раз.\n',
        SAFE_LOGIN_PASSWORD,
    ),
)

INCORRECT_FORMAT: Final[str] = ''.join(
    (
        'Некорректный формат. Повторите ввод логина и пароля.\n',
        SAFE_LOGIN_PASSWORD,
    ),
)

REQUIRED_AUTHORIZATION: Final[str] = ''.join(
    (
        'Требуется авторизация.\n',
        'Введите логин и пароль в формате: логин:пароль',
    ),
)

ACCEPTED_FORMAT_JSON: Final[str] = ''.join(
    'Принимаются файлы JSON, текст по формату и фотографии QR-кодов',
)

NOT_CREATE_ACCOUNT: Final[str] = ''.join(
    (
        'Не выбран счёт! ',
        'Сначала выберите его используя команду /select_account',
    ),
)
ERROR_DATABASE_RECORD: Final[str] = 'Ошибка записи в базу данных!'
ALREADY_LOGGED: Final[str] = ''.join(
    'Вы уже авторизованы! Повторная авторизация не требуется!',
)
ACCESS_DENIED: Final[str] = ''.join(
    (
        'У вас нет доступа к использованию бота, ',
        'сначала надо авторизоваться - /auth',
    ),
)
HELP_TEXT_START: Final[str] = ''.join(
    (
        'Описание команд:\n',
        '/start и /help выводят этот текст;\n',
        '/auth - позволяет авторизоваться в боте для доступа к ',
        'остальным командам;\n',
        '/select_account - выводит список счетов для выбора. ',
        'Счета добавляются через сайт;\n',
        '/manual - позволяет добавить чек с помощью параметров ',
        'самого чека, если, например, QR-код не считывается;\n'
        '/deauthorize - отвязывает телеграм аккаунт от бота.',
    ),
)
START_MANUAL_HANDLER_RECEIPT: Final[str] = ''.join(
    (
        'Чтобы добавить чек используя данные с чека, ',
        'введите поочередно - Дату в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС, ',
        'сумму чека, ФН, ФД, ФП.\n',
        'Сначала введите дату в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС',
    ),
)
NO_INFORMATION_BY_RECEIPT: Final[str] = ''.join(
    'Нет информации по чеку.\nПопробуйте позже или внесите данные на сайте',
)

# HTTP Status
SUCCESS_CODE: Final[int] = 200
SERVER_ERROR: Final[int] = 500
NOT_FOUND: Final[int] = 404
REDIRECTS: Final[int] = 302


# Числа
ONE: Final[int] = 1
TWO: Final[int] = 2
TEN: Final[int] = 10
TWENTY: Final[int] = 20
THIRTY: Final[int] = 30
FORTY: Final[int] = 40
FIFTY: Final[int] = 50
SIXTY: Final[int] = 60
SEVENTY: Final[int] = 70
EIGHTY: Final[int] = 80
NINTY: Final[int] = 90
ONE_HUNDRED: Final[int] = 100
ONE_HUNDRED_FIFTY: Final[int] = 150
TWO_HUNDRED: Final[int] = 200
TWO_HUNDRED_FIFTY: Final[int] = 250
DAY_MINUS_HOUR: Final[int] = 23
MINUTE_MINUS_ONE: Final[int] = 59
SECOND_MINUS_ONE: Final[int] = 59
TODAY_MINUS_FIVE_YEARS: Final[int] = 23
THREE_HUNDRED_SIXTY_FIVE: Final[int] = 365


# Порядковые номера месяцев
NUMBER_FIRST_MONTH_YEAR: Final[int] = 1
NUMBER_SECOND_MONTH_YEAR: Final[int] = 2
NUMBER_THIRD_MONTH_YEAR: Final[int] = 3
NUMBER_FOURTH_MONTH_YEAR: Final[int] = 4
NUMBER_FIFTH_MONTH_YEAR: Final[int] = 5
NUMBER_SIXTH_MONTH_YEAR: Final[int] = 6
NUMBER_SEVENTH_MONTH_YEAR: Final[int] = 7
NUMBER_EIGHTH_MONTH_YEAR: Final[int] = 8
NUMBER_NINTH_MONTH_YEAR: Final[int] = 9
NUMBER_TENTH_MONTH_YEAR: Final[int] = 10
NUMBER_ELEVENTH_MONTH_YEAR: Final[int] = 11
NUMBER_TWELFTH_MONTH_YEAR: Final[int] = 12

# Настройки Cookies
SESSION_COOKIE_AGE: Final[int] = 31536000

# Текст для ответов запросов
SUCCESS_WEBHOOKS: Final[str] = 'Webhook processed successfully'
WEBHOOKS_TELEGRAM: Final[str] = 'This page for Webhooks Telegram!'

# Параметры дат
TODAY = datetime.datetime.today()
CURRENT_YEAR = datetime.date.today().year


MONTH_NUMBERS: Final[dict] = {
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

MONTH_NAMES: Final[dict] = {
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
