# pylint: disable=missing-docstring, invalid-name
import sys
import re
import warnings
import django

__version__ = '0.10.0'

# Provide DepreciationWarning for older Python versions
# Have to use sys.version while supporting Python 3.5 to enable testing
# Once Python 3.5 is dropped can switch to version_info & compare tuples
if re.match(r'^3\.5', sys.version):
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
