"""Functions for general package configuration."""
import warnings

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from subscriptions.currency import Currency, CURRENCY


def string_to_module_and_class(string):
    """Breaks a string to a module and class name component."""
    components = string.split('.')
    component_class = components.pop()
    component_module = '.'.join(components)

    return {
        'module': component_module,
        'class': component_class,
    }


def validate_currency_settings(currency_locale):
    """Validates provided currency settings.

        Parameters
            currency_locale (str or dict): a currency locale string or
                a dictionary defining custom currency formating
                conventions.

        Raises:
            ImproperlyConfigured: specified string currency_locale not
                support.
            TypeError: invalid parameter type provided.
    """
    # STRING VALIDATION
    # ------------------------------------------------------------------------
    if isinstance(currency_locale, str):
        # Confirm that the provided locale is supported
        if currency_locale.lower() not in CURRENCY:
            raise ImproperlyConfigured(
                '{} is not a support DFS_CURRENCY_LOCALE value.'.format(currency_locale)
            )
    elif isinstance(currency_locale, dict):
        # Placeholder for any future specific dictionary validation
        pass
    else:
        raise TypeError(
            'Invalid DFS_CURRENCY_LOCALE type: {}. Must be str or dict.'.format(
                type(currency_locale)
            )
        )


def determine_currency_settings():
    """Determines details for Currency handling.

        Validates the provided currency locale setting and then returns
        a Currency object.

        Returns:
            obj: a Currency object for the provided setting.
    """
    # Get the proper setting attribute name
    # This block can be removed when DFS_CURRENCY_LOCALE has been
    # removed
    if hasattr(settings, 'DFS_CURRENCY'):
        currency_setting = 'DFS_CURRENCY'
    elif hasattr(settings, 'DFS_CURRENCY_LOCALE'):
        currency_setting = 'DFS_CURRENCY_LOCALE'

        deprecation_warning = (
            'DFS_CURRENCY_LOCALE is deprecated and has been replaced by '
            'DFS_CURRENCY. DFS_CURRENCY_LOCALE will be removed in a '
            'future version of django-flexible-subscription.'
        )
        warnings.warn(deprecation_warning, DeprecationWarning)
    else:
        currency_setting = 'DFS_CURRENCY'

    # Get the value for the currency
    currency_value = getattr(settings, currency_setting, 'en_us')

    # Validate currency locale setting
    validate_currency_settings(currency_value)

    # Return the Currency object
    return Currency(currency_value)


def compile_settings():
    """Compiles and validates all package settings and defaults.

        Provides basic checks to ensure required settings are declared
        and applies defaults for all missing settings.

        Returns:
            dict: All possible Django Flexible Subscriptions settings.
    """
    # ADMIN SETTINGS
    # -------------------------------------------------------------------------
    enable_admin = getattr(settings, 'DFS_ENABLE_ADMIN', False)

    # CURRENCY SETTINGS
    # -------------------------------------------------------------------------
    currency = determine_currency_settings()

    # TEMPLATE & VIEW SETTINGS
    # -------------------------------------------------------------------------
    base_template = getattr(
        settings, 'DFS_BASE_TEMPLATE', 'subscriptions/base.html'
    )

    # Get module and class for SubscribeView
    subscribe_view_path = getattr(
        settings, 'DFS_SUBSCRIBE_VIEW', 'subscriptions.views.SubscribeView'
    )
    subscribe_view = string_to_module_and_class(subscribe_view_path)

    # MANAGEMENT COMMANDS SETTINGS
    # ------------------------------------------------------------------------
    # Get module and class for the Management Command Manager class
    manager_object = getattr(
        settings,
        'DFS_MANAGER_CLASS',
        'subscriptions.management.commands._manager.Manager',
    )
    management_manager = string_to_module_and_class(manager_object)

    return {
        'enable_admin': enable_admin,
        'currency': currency,
        'base_template': base_template,
        'subscribe_view': subscribe_view,
        'management_manager': management_manager,
    }


SETTINGS = compile_settings()
