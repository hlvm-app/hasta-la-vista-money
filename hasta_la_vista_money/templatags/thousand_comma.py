from django import template

register = template.Library()

THOUSAND_MINUS_ONE = 999


@register.filter
def comma(number):
    if number > THOUSAND_MINUS_ONE:
        return str(
            number // 1000,
        ) + ' ' + str(number)[len(str(number // 1000)):]
    return number
