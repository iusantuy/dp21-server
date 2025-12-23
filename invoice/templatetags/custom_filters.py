# invoice/templatetags/custom_filters.py
from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def mul(value, arg):
    """Filter untuk mengalikan dua angka di template"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def rupiah(value):
    try:
        value = Decimal(value)
        return "{:,.0f}".format(value).replace(",", ".")
    except(ValueError, TypeError):    
        return value