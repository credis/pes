import datetime
from django import template
from django.template.defaultfilters import stringfilter
import re

register = template.Library()


@register.filter(name='todate')
def todate(value):
    if isinstance(value, int):
        return datetime.datetime.utcfromtimestamp(value / 1000)
    else:
        return value



@register.filter
@stringfilter
def skippage(url):
    res = re.sub(r'&page=(?P<num>[\d]+)', '',  url)
    return res

