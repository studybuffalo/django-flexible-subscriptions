"""Tests for the conf module."""
from django.conf import settings
from django.test import override_settings

from subscriptions.conf import compile_settings


@override_settings(
    SUBSCRIPTIONS_ENABLE_ADMIN=1,
    SUBSCRIPTIONS_CURRENCY_LOCALE=2,
)
def test_all_settings_populate_from_settings_properly():
    """Tests that Django settings all proper populate SETTINGS."""
    subscription_settings = compile_settings()

    assert len(subscription_settings) == 2
    assert subscription_settings['enable_admin'] == 1
    assert subscription_settings['currency_locale'] == '2'

@override_settings()
def test_settings_defaults():
    """Tests that SETTINGS adds all defaults properly."""
    # Clear any settings already provided
    del settings.SUBSCRIPTIONS_ENABLE_ADMIN
    del settings.SUBSCRIPTIONS_CURRENCY_LOCALE

    subscription_settings = compile_settings()

    assert len(subscription_settings) == 2
    assert subscription_settings['enable_admin'] is False
    assert subscription_settings['currency_locale'] == 'en_us'
