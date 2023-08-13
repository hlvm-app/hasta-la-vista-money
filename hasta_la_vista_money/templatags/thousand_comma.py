from typing import Union

from django import template

register = template.Library()

THOUSAND_MINUS_ONE = 999


@register.filter
def comma(number: float) -> Union[float, str]:
    """
    Функция разделения тысячных.

    :param number:
    :type number: float
    :return: Union[float, str]
    """
    if number > THOUSAND_MINUS_ONE:
        return (
            str(
                number // 1000,
            )
            + ' '
            + str(number)[len(str(number // 1000)) :]
        )
    return number
