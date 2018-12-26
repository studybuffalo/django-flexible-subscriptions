"""Tests for the __init__.py module."""
from importlib import reload
from unittest.mock import patch

import subscriptions

@patch('subscriptions.django.__version__', '1.11.0')
def test_django_111_depreciation_warning(recwarn):
    """Tests that the depreciation warning fires for Django 1.11."""
    reload(subscriptions)

    assert len(recwarn) == 1

    django_111_warning = recwarn.pop(DeprecationWarning)
    assert issubclass(django_111_warning.category, DeprecationWarning)

    warning_text = (
        'Django 1.11 LTS and django-flexible-subscriptions will '
        'stop receiving support in April 2020. Ensure you have '
        'updated your versions before then.'
    )

    assert str(django_111_warning.message) == warning_text

@patch('subscriptions.django.__version__', '2.0.0')
def test_other_django_versions_depreciation_warning(recwarn):
    """Tests that warning doesn't fire for other Django versions."""
    reload(subscriptions)

    assert len(recwarn) is 0
