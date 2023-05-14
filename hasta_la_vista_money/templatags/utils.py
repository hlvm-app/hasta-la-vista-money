from django import template

register = template.Library()


@register.filter
def comma(value):
    if value > 999:
        return str(value // 1000) + ' ' + str(value)[len(str(value // 1000)):]
    return value
