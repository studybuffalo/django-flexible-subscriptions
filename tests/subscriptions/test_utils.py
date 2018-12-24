"""Tests for the utils module."""
from datetime import datetime

import pytest

from django.contrib.auth.models import Group

from subscriptions import models, utils


@pytest.mark.django_db
def test_manager_process_expired_single_subscription(django_user_model):
    """Tests handling expiry with user with single subscription."""
    group = Group.objects.create(name='test')
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
        group=group
    )
    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=1, recurrence_unit=6, cost='1.00'
    )
    user = django_user_model.objects.create_user(username='a', password='b')
    group.user_set.add(user)
    user_count = group.user_set.all().count()
    subscription = models.UserSubscription.objects.create(
        user=user,
        subscription=cost,
        date_billing_start=datetime(2018, 1, 1, 1, 1, 1),
        date_billing_end=datetime(2018, 12, 31, 1, 1, 1),
        date_billing_last=datetime(2018, 12, 1, 1, 1, 1),
        date_billing_next=None,
        active=True,
        cancelled=False,
    )
    subscription_id = subscription.id

    manager = utils.Manager()
    manager.process_expired(subscription)
    subscription = models.UserSubscription.objects.get(id=subscription_id)
    assert group.user_set.all().count() == user_count - 1
    assert subscription.active is False
    assert subscription.cancelled is True
