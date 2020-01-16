# pylint: disable=missing-docstring, invalid-name
import sys
import warnings
import django

__version__ = '0.9.0'

# Provide DepreciationWarning for older Python versions
if sys.version_info[:2] == (3, 5):
    warnings.warn(
        (
            'django-flexible-subscription will stop supporting Python 3.5 '
            'once it reaches end-of-life (approximately September 2020). '
            'Ensure you have updated your Python version by then.'
        ),
        DeprecationWarning
    )
# Provide DepreciationWarning for older Django versions
if '1.11' in django.__version__:
    warnings.warn(
        (
            'django-flexible-subscription will stop supporting Django 1.11 LTS '
            'once it reaches end-of-life (approximately April 2020). '
            'Ensure you have updated your Django version by then.'
        ),
        DeprecationWarning
    )

# Django configuration details
default_app_config = 'subscriptions.apps.FlexibleSubscriptionsConfig'
