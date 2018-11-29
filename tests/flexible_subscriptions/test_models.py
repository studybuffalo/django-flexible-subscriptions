"""Tests for the models module."""
import pytest

from unittest import mock
from unittest.mock import patch

from subscriptions import models

class MockPaymentModel():
    def __init__(self):
        pass


# PlanTag Model
# -----------------------------------------------------------------------------
@pytest.mark.django_db
def test_plan_tag_minimal_model_creation():
    """Tests minimal requirements of PlanTag model."""
    models.PlanTag.objects.create(
        tag='Test Tag',
    )

    assert models.PlanTag.objects.all().count() == 1

@pytest.mark.django_db
def test_plan_tag_transaction_str():
    tag = models.PlanTag.objects.create(
        tag='Test Tag',
    )

    assert str(tag) == 'Test Tag'

# SubscriptionPlan Model
# -----------------------------------------------------------------------------
@pytest.mark.django_db
def test_subscription_plan_minimal_model_creation():
    """Tests minimal requirements of SubscriptionPlan model."""
    models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    assert models.SubscriptionPlan.objects.all().count() == 1

@pytest.mark.django_db
def test_subscription_plan_transaction_str():
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    assert str(plan) == 'Test Plan'

# PlanCost Model
# -----------------------------------------------------------------------------

# UserSubscription Model
# -----------------------------------------------------------------------------

# SubscriptionTransaction Model
# -----------------------------------------------------------------------------
