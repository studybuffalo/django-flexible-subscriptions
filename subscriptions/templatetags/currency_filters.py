"""Template filters for Django Flexible Subscriptions."""
from django import template

from subscriptions.conf import CURRENCY, SETTINGS


register = template.Library()

@register.filter(name='currency')
def currency(value):
    """Displays value as a currency based on the provided settings."""
    return CURRENCY[SETTINGS['currency_locale']].format_currency(value)
