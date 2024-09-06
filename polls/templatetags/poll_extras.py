from django import template

register = template.Library()


@register.filter(name='price')
def price(value):
    return '{:,}  تومان'.format(value)

@register.filter(name='price_sale')
def price_sale(value):
    return '{:,}'.format(value)