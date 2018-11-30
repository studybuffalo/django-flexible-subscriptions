"""Functions for general package configuration."""
from django.conf import settings

def compile_settings():
    """Compiles and validates all package settings and deaults.

        Provides basic checks to ensure required settings are declared
        and applies defaults for all missing settings.

        Returns:
            dict: All possible Django Flexible Subscriptions settings.
    """
    # ADMIN SETTINGS
    # -------------------------------------------------------------------------
    enable_admin = getattr(
        settings, 'SUBSCRIPTIONS_ENABLE_ADMIN', False
    )

    return {
        'enable_admin': enable_admin,
    }


SETTINGS = compile_settings()
