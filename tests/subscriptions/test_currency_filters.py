"""Tests the currency_filters module."""
from unittest.mock import patch

from subscriptions.templatetags.currency_filters import currency


@patch.dict('subscriptions.conf.SETTINGS', currency_locale='en_us')
def test_currency_filter():
    """Tests that value is properly returned as currency."""
    assert currency('1000.005') == '$1,000.01'
