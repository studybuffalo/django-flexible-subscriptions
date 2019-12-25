# pylint: disable=missing-docstring, invalid-name
__version__ = '0.8.1'

# Provide DepreciationWarning for older Django versions
import warnings

import django

if '1.11' in django.__version__:
    warnings.warn(
        (
            'Django 1.11 LTS and django-flexible-subscriptions will '
            'stop receiving support in April 2020. Ensure you have '
            'updated your versions before then.'
        ),
        DeprecationWarning
    )

# Django configuration details
default_app_config = 'subscriptions.apps.FlexibleSubscriptionsConfig'
