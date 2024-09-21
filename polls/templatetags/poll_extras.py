from django import template
from persiantools.jdatetime import JalaliDate, JalaliDateTime
import datetime
from datetime import datetime

register = template.Library()


@register.filter(name='price')
def price(value):
    return '{:,}  تومان'.format(value)


@register.filter(name='price_sale')
def price_sale(value):
    return '{:,}'.format(value)


@register.filter(name='times')
def jalali_data(value):
    s = str(value)
    gregorian_date = datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f%z")
    jalali_date = JalaliDateTime.to_jalali(gregorian_date)
    formatted_jalali_date = jalali_date.strftime("تاریخ : %Y/%m/%d   ساعت : %H:%M")
    return formatted_jalali_date
