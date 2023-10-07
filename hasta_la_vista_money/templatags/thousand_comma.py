from typing import Union

from django import template

register = template.Library()

THOUSAND_MINUS_ONE = 999
MILLION_MINUS_ONE = 999999


@register.filter
def comma(number: float) -> Union[float, str]:
    """
    Функция разделения тысячных и миллионных.

    :param number:
    :type number: float
    :return: Union[float, str]
    """
    if number > MILLION_MINUS_ONE:
        return f'{number:,.0f}'.replace(',', ' ')
    elif number > THOUSAND_MINUS_ONE:
        return f'{number:,.0f}'.replace(',', ' ')
    return number
