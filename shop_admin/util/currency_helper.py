from django import template
register = template.Library()

@register.filter
def to_currency(value):
    return float(value) / 100.0