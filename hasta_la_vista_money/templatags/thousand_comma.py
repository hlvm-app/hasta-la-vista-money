import decimal
from typing import Union

from django import template

register = template.Library()

THOUSAND_MINUS_ONE = 999


@register.filter
def comma(number: float) -> Union[float, str]:
    """
    Функция разделения тысячных и миллионных.

    :param number:
    :type number: float
    :return: Union[float, str]
    """
    return f'{decimal.Decimal(number):,.2f}'.replace(',', ' ')
