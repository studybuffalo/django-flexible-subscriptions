"""Template filters for Django Flexible Subscriptions."""
from django import template

from subscriptions.conf import SETTINGS


register = template.Library()


@register.filter(name='currency')
def currency(value):
    """Displays value as a currency based on the provided settings."""
    return SETTINGS['currency'].format_currency(value)
