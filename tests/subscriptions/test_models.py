"""Tests for the models module."""
from datetime import datetime

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

    assert cost.display_recurrent_unit_text == 'one-time'

@pytest.mark.django_db
def test_plan_cost_display_recurrent_unit_text_1():
    """Tests display_recurrent_unit_text for value 1."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_unit=models.SECOND
    )

    assert cost.display_recurrent_unit_text == 'per second'

@pytest.mark.django_db
def test_plan_cost_display_recurrent_unit_text_2():
    """Tests display_recurrent_unit_text for value 2."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_unit=models.MINUTE
    )

    assert cost.display_recurrent_unit_text == 'per minute'

@pytest.mark.django_db
def test_plan_cost_display_recurrent_unit_text_3():
    """Tests display_recurrent_unit_text for value 3."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_unit=models.HOUR
    )

    assert cost.display_recurrent_unit_text == 'per hour'

@pytest.mark.django_db
def test_plan_cost_display_recurrent_unit_text_4():
    """Tests display_recurrent_unit_text for value 4."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_unit=models.DAY
    )

    assert cost.display_recurrent_unit_text == 'per day'

@pytest.mark.django_db
def test_plan_cost_display_recurrent_unit_text_5():
    """Tests display_recurrent_unit_text for value 5."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_unit=models.WEEK
    )

    assert cost.display_recurrent_unit_text == 'per week'

@pytest.mark.django_db
def test_plan_cost_display_recurrent_unit_text_6():
    """Tests display_recurrent_unit_text for value 6."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_unit=models.MONTH
    )

    assert cost.display_recurrent_unit_text == 'per month'

@pytest.mark.django_db
def test_plan_cost_display_recurrent_unit_text_7():
    """Tests display_recurrent_unit_text for value 7."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_unit=models.YEAR
    )

    assert cost.display_recurrent_unit_text == 'per year'

@pytest.mark.django_db
def test_plan_cost_display_billing_frequency_text_once_singular():
    """Tests display_billing_frequency_text for singular one-time billing."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=1, recurrence_unit=models.ONCE
    )

    assert cost.display_billing_frequency_text == 'one-time'

@pytest.mark.django_db
def test_plan_cost_display_billing_frequency_text_once_plural():
    """Tests display_billing_frequency_text for plural one-time billing."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=2, recurrence_unit=models.ONCE
    )

    assert cost.display_billing_frequency_text == 'one-time'

@pytest.mark.django_db
def test_plan_cost_display_billing_frequency_text_second_singular():
    """Tests display_billing_frequency_text for singular per second billing."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=1, recurrence_unit=models.SECOND
    )

    assert cost.display_billing_frequency_text == 'per second'

@pytest.mark.django_db
def test_plan_cost_display_billing_frequency_text_second_plural():
    """Tests display_billing_frequency_text for plural per second billing."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=2, recurrence_unit=models.SECOND
    )

    assert cost.display_billing_frequency_text == 'every 2 seconds'

@pytest.mark.django_db
def test_plan_cost_display_billing_frequency_text_minute_singular():
    """Tests display_billing_frequency_text for singular per minute billing."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=1, recurrence_unit=models.MINUTE
    )

    assert cost.display_billing_frequency_text == 'per minute'

@pytest.mark.django_db
def test_plan_cost_display_billing_frequency_text_minute_plural():
    """Tests display_billing_frequency_text for plural per minute billing."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=2, recurrence_unit=models.MINUTE
    )

    assert cost.display_billing_frequency_text == 'every 2 minutes'

@pytest.mark.django_db
def test_plan_cost_display_billing_frequency_text_hour_singular():
    """Tests display_billing_frequency_text for singular per hour billing."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=1, recurrence_unit=models.HOUR
    )

    assert cost.display_billing_frequency_text == 'per hour'

@pytest.mark.django_db
def test_plan_cost_display_billing_frequency_text_hour_plural():
    """Tests display_billing_frequency_text for plural per hour billing."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=2, recurrence_unit=models.HOUR
    )

    assert cost.display_billing_frequency_text == 'every 2 hours'

@pytest.mark.django_db
def test_plan_cost_display_billing_frequency_text_day_singular():
    """Tests display_billing_frequency_text for singular per day billing."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=1, recurrence_unit=models.DAY
    )

    assert cost.display_billing_frequency_text == 'per day'

@pytest.mark.django_db
def test_plan_cost_display_billing_frequency_text_day_plural():
    """Tests display_billing_frequency_text for plural per day billing."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=2, recurrence_unit=models.DAY
    )

    assert cost.display_billing_frequency_text == 'every 2 days'

@pytest.mark.django_db
def test_plan_cost_display_billing_frequency_text_week_singular():
    """Tests display_billing_frequency_text for singular per week billing."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=1, recurrence_unit=models.WEEK
    )

    assert cost.display_billing_frequency_text == 'per week'

@pytest.mark.django_db
def test_plan_cost_display_billing_frequency_text_week_plural():
    """Tests display_billing_frequency_text for plural per week billing."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=2, recurrence_unit=models.WEEK
    )

    assert cost.display_billing_frequency_text == 'every 2 weeks'

@pytest.mark.django_db
def test_plan_cost_display_billing_frequency_text_month_singular():
    """Tests display_billing_frequency_text for singular per month billing."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=1, recurrence_unit=models.MONTH
    )

    assert cost.display_billing_frequency_text == 'per month'

@pytest.mark.django_db
def test_plan_cost_display_billing_frequency_text_month_plural():
    """Tests display_billing_frequency_text for plural per month billing."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=2, recurrence_unit=models.MONTH
    )

    assert cost.display_billing_frequency_text == 'every 2 months'

@pytest.mark.django_db
def test_plan_cost_display_billing_frequency_text_year_singular():
    """Tests display_billing_frequency_text for singular per year billing."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=1, recurrence_unit=models.YEAR
    )

    assert cost.display_billing_frequency_text == 'per year'

@pytest.mark.django_db
def test_plan_cost_display_billing_frequency_text_year_plural():
    """Tests display_billing_frequency_text for plural per year billing."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )

    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=2, recurrence_unit=models.YEAR
    )

    assert cost.display_billing_frequency_text == 'every 2 years'

@pytest.mark.django_db
def test_plan_cost_next_billing_datetime_seconds():
    """Tests next_billing_datetime with 'seconds'."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )
    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=1, recurrence_unit=models.SECOND
    )
    current = datetime(2018, 1, 1, 1, 1, 1)
    next_billing = cost.next_billing_datetime(current)

    assert next_billing == datetime(2018, 1, 1, 1, 1, 2)

@pytest.mark.django_db
def test_plan_cost_next_billing_datetime_minutes():
    """Tests next_billing_datetime with 'minutes'."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )
    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=1, recurrence_unit=models.MINUTE
    )
    current = datetime(2018, 1, 1, 1, 1, 1)
    next_billing = cost.next_billing_datetime(current)

    assert next_billing == datetime(2018, 1, 1, 1, 2, 1)

@pytest.mark.django_db
def test_plan_cost_next_billing_datetime_hours():
    """Tests next_billing_datetime with 'hours'."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )
    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=1, recurrence_unit=models.HOUR
    )
    current = datetime(2018, 1, 1, 1, 1, 1)
    next_billing = cost.next_billing_datetime(current)

    assert next_billing == datetime(2018, 1, 1, 2, 1, 1)

@pytest.mark.django_db
def test_plan_cost_next_billing_datetime_days():
    """Tests next_billing_datetime with 'days'."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )
    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=1, recurrence_unit=models.DAY
    )
    current = datetime(2018, 1, 1, 1, 1, 1)
    next_billing = cost.next_billing_datetime(current)

    assert next_billing == datetime(2018, 1, 2, 1, 1, 1)

@pytest.mark.django_db
def test_plan_cost_next_billing_datetime_weeks():
    """Tests next_billing_datetime with 'weeks'."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )
    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=1, recurrence_unit=models.WEEK
    )
    current = datetime(2018, 1, 1, 1, 1, 1)
    next_billing = cost.next_billing_datetime(current)

    assert next_billing == datetime(2018, 1, 8, 1, 1, 1)

@pytest.mark.django_db
def test_plan_cost_next_billing_datetime_months():
    """Tests next_billing_datetime with 'months'."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )
    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=1, recurrence_unit=models.MONTH
    )
    current = datetime(2018, 1, 1, 1, 1, 1)
    next_billing = cost.next_billing_datetime(current)

    assert next_billing == datetime(2018, 1, 31, 11, 30, 0, 520000)

@pytest.mark.django_db
def test_plan_cost_next_billing_datetime_12_months():
    """Tests next_billing_datetime with 'months'."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )
    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=12, recurrence_unit=models.MONTH
    )
    current = datetime(2018, 1, 1, 1, 1, 1)
    next_billing = cost.next_billing_datetime(current)

    assert next_billing == datetime(2019, 1, 1, 6, 48, 55, 240000)

@pytest.mark.django_db
def test_plan_cost_next_billing_datetime_48_months():
    """Tests next_billing_datetime with 12 'months'."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )
    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=48, recurrence_unit=models.MONTH
    )
    current = datetime(2018, 1, 1, 1, 1, 1)
    next_billing = cost.next_billing_datetime(current)

    assert next_billing == datetime(2022, 1, 1, 0, 12, 37, 960000)

@pytest.mark.django_db
def test_plan_cost_next_billing_datetime_years():
    """Tests next_billing_datetime with 48 'months'."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )
    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=1, recurrence_unit=models.YEAR
    )
    current = datetime(2018, 1, 1, 1, 1, 1)
    next_billing = cost.next_billing_datetime(current)

    assert next_billing == datetime(2019, 1, 1, 6, 50, 13)

@pytest.mark.django_db
def test_plan_cost_next_billing_datetime_4_years():
    """Tests next_billing_datetime with 4 'years'."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )
    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=4, recurrence_unit=models.YEAR
    )
    current = datetime(2018, 1, 1, 1, 1, 1)
    next_billing = cost.next_billing_datetime(current)

    assert next_billing == datetime(2022, 1, 1, 0, 17, 49)

@pytest.mark.django_db
def test_plan_cost_next_billing_datetime_once():
    """Tests next_billing_datetime with period of 'once'."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='This is a test plan',
    )
    cost = models.PlanCost.objects.create(
        plan=plan, recurrence_period=1, recurrence_unit=models.ONCE
    )
    current = datetime(2018, 1, 1, 1, 1, 1)
    next_billing = cost.next_billing_datetime(current)

    assert next_billing is None

# PlanList Model
# -----------------------------------------------------------------------------
@pytest.mark.django_db
def test_plan_list_minimal_model_creation():
    """Tests minimal requirements of PlanList model."""
    models.PlanList.objects.create(
        title='Test Title',
    )

    assert models.PlanList.objects.all().count() == 1

@pytest.mark.django_db
def test_plan_list_str():
    """Tests __str__ for the PlanList model."""
    plan_list = models.PlanList.objects.create(
        title='Test Title',
    )

    assert str(plan_list) == 'Test Title'

# PlanListDetails Model
# -----------------------------------------------------------------------------
@pytest.mark.django_db
def test_plan_list_details_minimal_model_creation():
    """Tests minimal requirements of PlanListDetails model."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='A test plan',
    )
    plan_list = models.PlanList.objects.create(
        title='Test Title',
    )
    models.PlanListDetail.objects.create(
        plan=plan,
        plan_list=plan_list,
    )

    assert models.PlanListDetail.objects.all().count() == 1

@pytest.mark.django_db
def test_plan_list_details_str():
    """Tests __str__ for the PlanListDetails model."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='Test Plan',
        plan_description='A test plan',
    )
    plan_list = models.PlanList.objects.create(
        title='Test Title',
    )
    plan_list_details = models.PlanListDetail.objects.create(
        plan=plan,
        plan_list=plan_list,
        title='Test Plan as part of Test List',
    )

    assert str(plan_list_details) == 'Test Plan as part of Test List'
