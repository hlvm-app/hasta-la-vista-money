import decimal

from django import template

register = template.Library()

THOUSAND_MINUS_ONE = 999


@register.filter
def comma(number: float) -> str:
    """
    Функция разделения тысячных и миллионных.

    :param number:
    :type number: float
    :return: str
    """
    return f'{decimal.Decimal(number):,.2f}'.replace(',', ' ')
