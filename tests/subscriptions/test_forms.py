"""Tests for the models module."""
from datetime import datetime
from unittest.mock import patch, MagicMock
from uuid import uuid4

import pytest

from subscriptions import forms, models


pytestmark = pytest.mark.django_db  # pylint: disable=invalid-name

def create_plan(plan_name='1', plan_description='2'):
    """Creates and returns SubscriptionPlan instance."""
    return models.SubscriptionPlan.objects.create(
        plan_name=plan_name, plan_description=plan_description
    )

def create_cost(plan=None, period=1, unit=models.MONTH, cost='1.00'):
    """Creates and returns PlanCost instance."""
    return models.PlanCost.objects.create(
        plan=plan, recurrence_period=period, recurrence_unit=unit, cost=cost
    )

# General Functions
# -----------------------------------------------------------------------------
@patch(
    'subscriptions.forms.timezone.now',
    MagicMock(return_value=datetime(2000, 1, 1))
)
def test_assemble_cc_years_correct_output():
    """Tests that assemble_cc_years returns the expected 60 years of data."""
    cc_years = forms.assemble_cc_years()

    assert len(cc_years) == 60
    assert cc_years[0] == (2000, 2000)
    assert cc_years[-1] == (2059, 2059)

# SubscriptionPlanCostForm
# -----------------------------------------------------------------------------
def test_subscription_plan_cost_form_with_plan():
    """Tests minimal creation of SubscriptionPlanCostForm."""
    plan = create_plan()
    create_cost(plan=plan)

    try:
        forms.SubscriptionPlanCostForm(subscription_plan=plan)
    except KeyError:
        assert False
    else:
        assert True

def test_subscription_plan_cost_form_without_plan():
    """Tests that SubscriptionPlanCostForm requires a plan."""
    try:
        forms.SubscriptionPlanCostForm()
    except KeyError:
        assert True
    else:
        assert False

def test_subscription_plan_cost_form_proper_widget_values():
    """Tests that widget values are properly added."""
    plan = create_plan()
    create_cost(plan, period=3, unit=models.HOUR, cost='3.00')
    create_cost(plan, period=1, unit=models.SECOND, cost='1.00')
    create_cost(plan, period=2, unit=models.MINUTE, cost='2.00')

    form = forms.SubscriptionPlanCostForm(subscription_plan=plan)
    choices = form.fields['plan_cost'].widget.choices
    assert choices[0][1] == '$1.00 per second'
    assert choices[1][1] == '$2.00 every 2 minutes'
    assert choices[2][1] == '$3.00 every 3 hours'

def test_subscription_plan_cost_form_clean_plan_cost_value():
    """Tests that clean returns PlanCost instance."""
    plan = create_plan()
    cost = create_cost(plan=plan)
    cost_form = forms.SubscriptionPlanCostForm(
        {'plan_cost': str(cost.id)}, subscription_plan=plan
    )

    assert cost_form.is_valid()
    assert cost_form.cleaned_data['plan_cost'] == cost

def test_subscription_plan_cost_form_clean_plan_cost_invalid_uuid():
    """Tests that clean_pan_cost returns error if instance not found."""
    plan = create_plan()
    create_cost(plan=plan)
    cost_form = forms.SubscriptionPlanCostForm(
        {'plan_cost': str(uuid4())}, subscription_plan=plan
    )

    assert cost_form.is_valid() is False
    assert cost_form.errors == {'plan_cost': ['Invalid plan cost submitted.']}
