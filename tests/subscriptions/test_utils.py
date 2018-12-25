"""Tests for the utils module."""
from datetime import datetime
from unittest.mock import patch

import pytest

from django.contrib.auth.models import Group

from subscriptions import models, utils


def create_cost(group):
    """Creates and returns a PlanCost instance."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
        group=group
    )

    return models.PlanCost.objects.create(
        plan=plan, recurrence_period=1, recurrence_unit=6, cost='1.00'
    )

@pytest.mark.django_db
def test_manager_process_expired_single_group(django_user_model):
    """Tests handling expiry with user with single group."""
    user = django_user_model.objects.create_user(username='a', password='b')
    group = Group.objects.create(name='test')
    group.user_set.add(user)
    user_count = group.user_set.all().count()

    cost = create_cost(group)
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

@pytest.mark.django_db
def test_manager_process_expired_multiple_different_groups(django_user_model):
    """Tests handling expiry with user with multiple different groups."""
    user = django_user_model.objects.create_user(username='a', password='b')

    group_1 = Group.objects.create(name='test_1')
    group_1.user_set.add(user)
    user_count_1 = group_1.user_set.all().count()
    group_2 = Group.objects.create(name='test_2')
    group_2.user_set.add(user)
    user_count_2 = group_1.user_set.all().count()

    cost_1 = create_cost(group_1)
    subscription_1 = models.UserSubscription.objects.create(
        user=user,
        subscription=cost_1,
        date_billing_start=datetime(2018, 1, 1, 1, 1, 1),
        date_billing_end=datetime(2018, 12, 31, 1, 1, 1),
        date_billing_last=datetime(2018, 12, 1, 1, 1, 1),
        date_billing_next=None,
        active=True,
        cancelled=False,
    )
    subscription_1_id = subscription_1.id
    cost_2 = create_cost(group_2)
    subscription_2 = models.UserSubscription.objects.create(
        user=user,
        subscription=cost_2,
        date_billing_start=datetime(2018, 1, 1, 1, 1, 1),
        date_billing_end=datetime(2018, 12, 31, 1, 1, 1),
        date_billing_last=datetime(2018, 12, 1, 1, 1, 1),
        date_billing_next=None,
        active=True,
        cancelled=False,
    )
    subscription_2_id = subscription_2.id

    manager = utils.Manager()
    manager.process_expired(subscription_1)

    subscription_1 = models.UserSubscription.objects.get(id=subscription_1_id)
    subscription_2 = models.UserSubscription.objects.get(id=subscription_2_id)

    assert group_1.user_set.all().count() == user_count_1 - 1
    assert group_2.user_set.all().count() == user_count_2
    assert subscription_1.active is False
    assert subscription_1.cancelled is True
    assert subscription_2.active is True
    assert subscription_2.cancelled is False

@pytest.mark.django_db
def test_manager_process_expired_multiple_same_groups(django_user_model):
    """Tests handling expiry with user with multiple same groups."""
    user = django_user_model.objects.create_user(username='a', password='b')

    group = Group.objects.create(name='test_1')
    user_count = group.user_set.all().count()

    cost_1 = create_cost(group)
    subscription_1 = models.UserSubscription.objects.create(
        user=user,
        subscription=cost_1,
        date_billing_start=datetime(2018, 1, 1, 1, 1, 1),
        date_billing_end=datetime(2018, 12, 31, 1, 1, 1),
        date_billing_last=datetime(2018, 12, 1, 1, 1, 1),
        date_billing_next=None,
        active=True,
        cancelled=False,
    )
    subscription_1_id = subscription_1.id
    cost_2 = create_cost(group)
    subscription_2 = models.UserSubscription.objects.create(
        user=user,
        subscription=cost_2,
        date_billing_start=datetime(2018, 1, 1, 1, 1, 1),
        date_billing_end=datetime(2018, 12, 31, 1, 1, 1),
        date_billing_last=datetime(2018, 12, 1, 1, 1, 1),
        date_billing_next=None,
        active=True,
        cancelled=False,
    )
    subscription_2_id = subscription_2.id

    manager = utils.Manager()
    manager.process_expired(subscription_1)

    subscription_1 = models.UserSubscription.objects.get(id=subscription_1_id)
    subscription_2 = models.UserSubscription.objects.get(id=subscription_2_id)

    assert group.user_set.all().count() == user_count
    assert subscription_1.active is False
    assert subscription_1.cancelled is True
    assert subscription_2.active is True
    assert subscription_2.cancelled is False

@pytest.mark.django_db
def test_manager_process_new_with_group(django_user_model):
    """Tests processing of new subscription with group."""
    user = django_user_model.objects.create_user(username='a', password='b')
    group = Group.objects.create(name='test')
    user_count = group.user_set.all().count()

    cost = create_cost(group)
    subscription = models.UserSubscription.objects.create(
        user=user,
        subscription=cost,
        date_billing_start=datetime(2018, 1, 1, 1, 1, 1),
        date_billing_end=datetime(2018, 12, 31, 1, 1, 1),
        date_billing_last=datetime(2018, 12, 1, 1, 1, 1),
        date_billing_next=None,
        active=False,
        cancelled=False,
    )
    subscription_id = subscription.id

    manager = utils.Manager()
    manager.process_new(subscription)

    subscription = models.UserSubscription.objects.get(id=subscription_id)

    assert group.user_set.all().count() == user_count + 1
    assert subscription.active is True
    assert subscription.cancelled is False

@pytest.mark.django_db
def test_manager_process_new_without_group(django_user_model):
    """Tests processing of new subscription without group."""
    user = django_user_model.objects.create_user(username='a', password='b')
    cost = create_cost(None)
    subscription = models.UserSubscription.objects.create(
        user=user,
        subscription=cost,
        date_billing_start=datetime(2018, 1, 1, 1, 1, 1),
        date_billing_end=datetime(2018, 12, 31, 1, 1, 1),
        date_billing_last=datetime(2018, 12, 1, 1, 1, 1),
        date_billing_next=None,
        active=False,
        cancelled=False,
    )
    subscription_id = subscription.id

    manager = utils.Manager()
    manager.process_new(subscription)

    subscription = models.UserSubscription.objects.get(id=subscription_id)

    assert subscription.active is True
    assert subscription.cancelled is False

@patch('subscriptions.utils.Manager.process_payment', lambda x, y, z: False)
@pytest.mark.django_db
def test_manager_process_new_payment_error(django_user_model):
    """Tests handlig of new subscription payment error."""
    user = django_user_model.objects.create_user(username='a', password='b')
    cost = create_cost(None)
    subscription = models.UserSubscription.objects.create(
        user=user,
        subscription=cost,
        date_billing_start=datetime(2018, 1, 1, 1, 1, 1),
        date_billing_end=datetime(2018, 12, 31, 1, 1, 1),
        date_billing_last=datetime(2018, 12, 1, 1, 1, 1),
        date_billing_next=None,
        active=False,
        cancelled=False,
    )
    subscription_id = subscription.id

    manager = utils.Manager()
    manager.process_new(subscription)

    subscription = models.UserSubscription.objects.get(id=subscription_id)

    assert subscription.date_billing_next is None
    assert subscription.active is False
    assert subscription.cancelled is False

@patch('subscriptions.utils.timezone.now', lambda: datetime(2019, 1, 1))
@pytest.mark.django_db
def test_manager_process_subsriptions_with_expired(django_user_model):
    """Tests that process_susbscriptions processes expiries."""
    user = django_user_model.objects.create_user(username='a', password='b')
    group = Group.objects.create(name='test')
    group.user_set.add(user)
    user_count = group.user_set.all().count()

    cost = create_cost(group)
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
    manager.process_subscriptions()

    subscription = models.UserSubscription.objects.get(id=subscription_id)

    assert group.user_set.all().count() == user_count - 1
    assert subscription.active is False
    assert subscription.cancelled is True

@patch('subscriptions.utils.timezone.now', lambda: datetime(2018, 1, 2))
@pytest.mark.django_db
def test_manager_process_subscriptions_with_new(django_user_model):
    """Tests processing of new subscription via process_subscriptions."""
    user = django_user_model.objects.create_user(username='a', password='b')
    group = Group.objects.create(name='test')
    user_count = group.user_set.all().count()

    cost = create_cost(group)
    subscription = models.UserSubscription.objects.create(
        user=user,
        subscription=cost,
        date_billing_start=datetime(2018, 1, 1, 1, 1, 1),
        date_billing_end=datetime(2018, 12, 31, 1, 1, 1),
        date_billing_last=None,
        date_billing_next=None,
        active=False,
        cancelled=False,
    )
    subscription_id = subscription.id

    manager = utils.Manager()
    manager.process_subscriptions()

    subscription = models.UserSubscription.objects.get(id=subscription_id)

    assert group.user_set.all().count() == user_count + 1
    assert subscription.active is True
    assert subscription.cancelled is False

@patch('subscriptions.utils.timezone.now', lambda: datetime(2018, 12, 2))
@pytest.mark.django_db
def test_manager_process_subscriptions_with_due(django_user_model):
    """Tests processing of subscriptions with billing due."""
    user = django_user_model.objects.create_user(username='a', password='b')
    group = Group.objects.create(name='test')
    user_count = group.user_set.all().count()

    cost = create_cost(group)
    subscription = models.UserSubscription.objects.create(
        user=user,
        subscription=cost,
        date_billing_start=datetime(2018, 1, 1, 1, 1, 1),
        date_billing_end=datetime(2018, 12, 31, 1, 1, 1),
        date_billing_last=datetime(2018, 11, 1, 1, 1, 1),
        date_billing_next=datetime(2018, 12, 1, 1, 1, 1),
        active=True,
        cancelled=False,
    )
    subscription_id = subscription.id

    manager = utils.Manager()
    manager.process_subscriptions()

    subscription = models.UserSubscription.objects.get(id=subscription_id)

    assert group.user_set.all().count() == user_count
    assert subscription.active is True
    assert subscription.cancelled is False
