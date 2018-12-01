"""Tests for the models module."""
import pytest

from subscriptions import models


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
    """Tests __str__ for the PlanTag model."""
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
    "Tests __str__ for the SubscriptionPlan model."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    assert str(plan) == 'Test Plan'

@pytest.mark.django_db
def test_subscription_plan_transaction_display_tags_0():
    """Tests display_tags or SubscriptionPlan with 0 tags."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    assert plan.display_tags() == ''

@pytest.mark.django_db
def test_subscription_plan_transaction_display_tags_1():
    """Tests display_tags or SubscriptionPlan with 1 tag."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    tag_1 = models.PlanTag.objects.create(tag='tag 1')
    plan.tags.add(tag_1)

    assert plan.display_tags() == 'tag 1'

@pytest.mark.django_db
def test_subscription_plan_transaction_display_tags_2():
    """Tests display_tags or SubscriptionPlan with 2 tags."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    tag_1 = models.PlanTag.objects.create(tag='tag 1')
    tag_2 = models.PlanTag.objects.create(tag='tag 2')
    plan.tags.add(tag_1)
    plan.tags.add(tag_2)

    assert plan.display_tags() == 'tag 1, tag 2'

@pytest.mark.django_db
def test_subscription_plan_transaction_display_tags_3():
    """Tests display_tags or SubscriptionPlan with 3 tags."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    tag_1 = models.PlanTag.objects.create(tag='tag 1')
    tag_2 = models.PlanTag.objects.create(tag='tag 2')
    tag_3 = models.PlanTag.objects.create(tag='tag 3')
    plan.tags.add(tag_1)
    plan.tags.add(tag_2)
    plan.tags.add(tag_3)

    assert plan.display_tags() == 'tag 1, tag 2, tag 3'

@pytest.mark.django_db
def test_subscription_plan_transaction_display_tags_4():
    """Tests display_tags or SubscriptionPlan with 4 tags."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    tag_1 = models.PlanTag.objects.create(tag='tag 1')
    tag_2 = models.PlanTag.objects.create(tag='tag 2')
    tag_3 = models.PlanTag.objects.create(tag='tag 3')
    tag_4 = models.PlanTag.objects.create(tag='tag 4')
    plan.tags.add(tag_1)
    plan.tags.add(tag_2)
    plan.tags.add(tag_3)
    plan.tags.add(tag_4)

    assert plan.display_tags() == 'tag 1, tag 2, tag 3, ...'

# PlanTag Model
# -----------------------------------------------------------------------------
def test_plan_cost_convenience_unit_reference():
    """Confirms convenience unit references are correct."""
    assert models.ONCE == 0
    assert models.SECOND == 1
    assert models.MINUTE == 2
    assert models.HOUR == 3
    assert models.DAY == 4
    assert models.WEEK == 5
    assert models.MONTH == 6
    assert models.YEAR == 7

@pytest.mark.django_db
def test_plan_cost_minimal_model_creation():
    """Tests minimal requirements of PlanCost model."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    models.PlanCost.objects.create(
        plan=plan,
        recurrence_period=1,
        recurrence_unit=models.SECOND,
        cost='1.00',
    )

    assert models.PlanCost.objects.all().count() == 1

@pytest.mark.django_db
def test_plan_cost_display_recurrent_unit_text_0():
    """Tests display_recurrent_unit_text for value 0."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_unit=models.ONCE
    )

    assert cost.display_recurrent_unit_text() == 'one-time'
