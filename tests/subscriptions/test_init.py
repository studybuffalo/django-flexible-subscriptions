"""Tests for the __init__.py module."""
from importlib import reload
from unittest.mock import patch

import subscriptions


@patch('subscriptions.sys.version', '3.5.1')
@patch('subscriptions.django.__version__', '3.0.0')
def test_python_35_depreciation_warning(recwarn):
    """Tests that depreciation warning fires for Python 3.5.x"""
    reload(subscriptions)

    assert len(recwarn) == 1

    django_111_warning = recwarn.pop(DeprecationWarning)
    assert issubclass(django_111_warning.category, DeprecationWarning)

    warning_text = (
        'django-flexible-subscription will stop supporting Python 3.5 '
        'once it reaches end-of-life (approximately September 2020). '
        'Ensure you have updated your Python version by then.'
    )

    assert str(django_111_warning.message) == warning_text

@patch('subscriptions.sys.version', '3.6.0')
@patch('subscriptions.django.__version__', '3.0.0')
def test_other_python_versions_depreciation_warning(recwarn):
    """Tests that warning doesn't fire for other Python versions."""
    reload(subscriptions)

    assert len(recwarn) is 0

@patch('subscriptions.sys.version', '3.6.0')
@patch('subscriptions.django.__version__', '1.11.0')
def test_django_111_depreciation_warning(recwarn):
    """Tests that the depreciation warning fires for Django 1.11."""
    reload(subscriptions)

    assert len(recwarn) == 1

    django_111_warning = recwarn.pop(DeprecationWarning)
    assert issubclass(django_111_warning.category, DeprecationWarning)

    warning_text = (
        'django-flexible-subscription will stop supporting Django 1.11 LTS '
        'once it reaches end-of-life (approximately April 2020). '
        'Ensure you have updated your Django version by then.'
    )

    assert str(django_111_warning.message) == warning_text

@patch('subscriptions.sys.version', '3.6.0')
@patch('subscriptions.django.__version__', '2.0.0')
def test_other_django_versions_depreciation_warning(recwarn):
    """Tests that warning doesn't fire for other Django versions."""
    reload(subscriptions)

    assert len(recwarn) is 0
