"""Tests for the models module."""
import pytest

from subscriptions import forms, models


def create_plan(plan_name='1', plan_description='2'):
    """Creates and returns SubscriptionPlan instance."""
    return models.SubscriptionPlan.objects.create(
        plan_name=plan_name, plan_description=plan_description
    )

def create_cost(plan=None, period=1, unit=6, cost='1.00'):
    """Creates and returns PlanCost instance."""
    return models.PlanCost.objects.create(
        plan=plan, recurrence_period=period, recurrence_unit=unit, cost=cost
    )

# SubscriptionPlanCostForm
# -----------------------------------------------------------------------------
@pytest.mark.django_db
def test_subscription_plan_cost_form_with_plan():
    """Tests minimal creation of SubscriptionPlanCostForm."""
    plan = create_plan()

    try:
        forms.SubscriptionPlanCostForm(subscription_plan=plan)
    except KeyError:
        assert False
    else:
        assert True

@pytest.mark.django_db
def test_subscription_plan_cost_form_without_plan():
    """Tests that SubscriptionPlanCostForm requires a plan."""
    try:
        forms.SubscriptionPlanCostForm()
    except KeyError:
        assert True
    else:
        assert False

@pytest.mark.django_db
def test_subscription_plan_cost_form_proper_widget_values():
    """Tests that widget values are properly added."""
    plan = create_plan()
    create_cost(plan, period=3, unit=3, cost='3.00')
    create_cost(plan, period=1, unit=1, cost='1.00')
    create_cost(plan, period=2, unit=2, cost='2.00')

    form = forms.SubscriptionPlanCostForm(subscription_plan=plan)
    choices = form.fields['plan_cost'].widget.choices
    assert choices[0][1] == '$1.00 per second'
    assert choices[1][1] == '$2.00 every 2 minutes'
    assert choices[2][1] == '$3.00 every 3 hours'
