"""Tests for the conf module."""
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

from subscriptions import conf


def test__string_to_module_and_class__one_period():
    """Tests handling of string with single period."""
    string = 'a.b'
    components = conf.string_to_module_and_class(string)

    assert components['module'] == 'a'
    assert components['class'] == 'b'


def test__string_to_module_and_class__two_periods():
    """Tests handling of string with more than one period."""
    string = 'a.b.c'
    components = conf.string_to_module_and_class(string)

    assert components['module'] == 'a.b'
    assert components['class'] == 'c'


def test__validate_currency_settings__valid_str():
    """Confirms no error when valid currency_locale string provided."""
    try:
        conf.validate_currency_settings('en_us')
    except ImproperlyConfigured:
        assert False
    else:
        assert True


def test__validate_currency_settings__invalid_str():
    """Confirms error when invalid currency_locale string provided."""
    try:
        conf.validate_currency_settings('1')
    except ImproperlyConfigured as error:
        assert str(error) == '1 is not a support DFS_CURRENCY_LOCALE value.'
    else:
        assert False


def test__validate_currency_settings__valid_dict():
    """Confirms no error when valid currency_locale string provided."""
    try:
        conf.validate_currency_settings({})
    except ImproperlyConfigured:
        assert False
    else:
        assert True


def test__validate_currency_settings__invalid_type():
    """Confirms error when invalid currency_locale string provided."""
    try:
        conf.validate_currency_settings(True)
    except TypeError as error:
        assert str(error) == (
            "Invalid DFS_CURRENCY_LOCALE type: <class 'bool'>. Must be str or dict."
        )
    else:
        assert False


@override_settings(
    DFS_CURRENCY='en_us',
)
def test__determine_currency_settings__dfs_currency_declared():
    """Confirms handling when DFS_CURRENCY declared."""
    # Clear any conflicting settings already provided
    del settings.DFS_CURRENCY_LOCALE

    currency_object = conf.determine_currency_settings()

    # Confirm a currency object was returned
    assert currency_object.locale == 'en_us'


@override_settings(
    DFS_CURRENCY_LOCALE={},
)
def test__determine_currency_settings__dfs_currency_locale_declared(recwarn):
    """Confirms handling when DFS_CURRENCY_LOCALE declared."""
    # Clear any conflicting settings already provided
    del settings.DFS_CURRENCY

    currency_object = conf.determine_currency_settings()

    # Confirm a currency object was returned
    assert currency_object.locale == 'custom'

    # Confirm DeprecationWarning was raised
    currency_warning = recwarn.pop(DeprecationWarning)
    assert issubclass(currency_warning.category, DeprecationWarning)

    warning_text = (
        'DFS_CURRENCY_LOCALE is deprecated and has been replaced by '
        'DFS_CURRENCY. DFS_CURRENCY_LOCALE will be removed in a '
        'future version of django-flexible-subscription.'
    )
    assert str(currency_warning.message) == warning_text


@override_settings()
def test__determine_currency_settings__not_declared():
    """Confirms handling when currency is not declared."""
    # Clear any settings already provided
    del settings.DFS_CURRENCY
    del settings.DFS_CURRENCY_LOCALE

    currency_object = conf.determine_currency_settings()

    # Confirm the default currency object was returned
    assert currency_object.locale == 'en_us'


@override_settings(
    DFS_ENABLE_ADMIN=1,
    DFS_CURRENCY='en_us',
    DFS_BASE_TEMPLATE='3',
    DFS_SUBSCRIBE_VIEW='a.b',
    DFS_MANAGER_CLASS='a.b',
)
def test__compile_settings__assigned_properly():
    """Tests that Django settings all proper populate SETTINGS."""
    subscription_settings = conf.compile_settings()

    assert len(subscription_settings) == 5
    assert subscription_settings['enable_admin'] == 1
    assert subscription_settings['currency'].locale == 'en_us'
    assert subscription_settings['base_template'] == '3'
    assert subscription_settings['subscribe_view']['module'] == 'a'
    assert subscription_settings['subscribe_view']['class'] == 'b'
    assert subscription_settings['management_manager']['module'] == 'a'
    assert subscription_settings['management_manager']['class'] == 'b'


@override_settings()
def test__compile_settings__defaults():
    """Tests that SETTINGS adds all defaults properly."""
    # Clear any settings already provided
    del settings.DFS_ENABLE_ADMIN
    del settings.DFS_CURRENCY
    del settings.DFS_BASE_TEMPLATE
    del settings.DFS_SUBSCRIBE_VIEW
    del settings.DFS_MANAGER_CLASS

    subscription_settings = conf.compile_settings()

    assert len(subscription_settings) == 5
    assert subscription_settings['enable_admin'] is False
    assert subscription_settings['currency'].locale == 'en_us'
    assert subscription_settings['base_template'] == 'subscriptions/base.html'
    assert subscription_settings['subscribe_view']['module'] == (
        'subscriptions.views'
    )
    assert subscription_settings['subscribe_view']['class'] == (
        'SubscribeView'
    )
    assert subscription_settings['management_manager']['module'] == (
        'subscriptions.management.commands._manager'
    )
    assert subscription_settings['management_manager']['class'] == (
        'Manager'
    )

