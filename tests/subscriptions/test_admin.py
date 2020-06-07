"""Tests for the Subscriptions admin module."""
from importlib import reload
from unittest.mock import patch

from django.contrib import admin

from subscriptions import admin as subscription_admin, models


@patch.dict('subscriptions.conf.SETTINGS', {'enable_admin': True})
def test_admin_included_when_true_in_settings():
    """Tests that admin views are loaded when enabled in settings."""
    # pylint: disable=protected-access
    reload(subscription_admin)

    try:
        admin.site._registry[models.SubscriptionPlan]
    except KeyError:
        assert False
    else:
        # Remove the registered model to prevent impacting other tests
        admin.site._registry.pop(models.SubscriptionPlan)
        assert True

    try:
        admin.site._registry[models.UserSubscription]
    except KeyError:
        assert False
    else:
        # Remove the registered model to prevent impacting other tests
        admin.site._registry.pop(models.UserSubscription)
        assert True

    try:
        admin.site._registry[models.SubscriptionTransaction]
    except KeyError:
        assert False
    else:
        # Remove the registered model to prevent impacting other tests
        admin.site._registry.pop(models.SubscriptionTransaction)
        assert True


@patch.dict('subscriptions.conf.SETTINGS', {'enable_admin': False})
def test_admin_excluded_when_false_in_settings():
    """Tests that admin views are not loaded when disabled in settings."""
    # pylint: disable=protected-access
    reload(subscription_admin)

    try:
        admin.site._registry[models.SubscriptionPlan]
    except KeyError:
        assert True
    else:
        assert False

    try:
        admin.site._registry[models.UserSubscription]
    except KeyError:
        assert True
    else:
        assert False
    try:
        admin.site._registry[models.SubscriptionTransaction]
    except KeyError:
        assert True
    else:
        assert False
