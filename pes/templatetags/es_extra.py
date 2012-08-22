import datetime
from django import template

register = template.Library()


@register.filter(name='todate')
def todate(value):
    if isinstance(value, int):
        return datetime.datetime.utcfromtimestamp(value / 1000)
    else:
        return value

