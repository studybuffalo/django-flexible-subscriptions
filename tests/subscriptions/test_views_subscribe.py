"""Tests for the django-flexible-subscriptions UserSubscription views."""
import pytest

from django.urls import reverse

from subscriptions import models, views


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


def test_subscribe_view_get_context_dataa_override():
    """Tests that get_context_data override works properly."""
    view = views.SubscribeView()
    context = view.get_context_data()

    assert context['template_extends'] == 'subscriptions/base.html'

def test_subscribe_view_get_template_names_override_confirmation_true():
    """Tests get_template_names override works when confirmation is true."""
    view = views.SubscribeView()
    view.confirmation = True
    template = view.get_template_names()

    assert template == ['subscriptions/subscribe_confirmation.html']

def test_subscribe_view_get_template_names_override_confirmation_false():
    """Tests get_template_names override works when confirmation is false."""
    view = views.SubscribeView()
    view.confirmation = False
    template = view.get_template_names()

    assert template == ['subscriptions/subscribe_preview.html']

def test_subscribe_view_get_success_url():
    """Tests get_success_url method works as expected."""
    view = views.SubscribeView()
    success_url = view.get_success_url()

    assert success_url == '/'

@pytest.mark.django_db
def test_subscribe_view_post_404_with_missing_plan(admin_client):
    """Tests post returns 404 response when plan is missing."""
    post_data = {
        'action': None,
    }

    response = admin_client.post(
        reverse('subscriptions_subscribe'),
        post_data,
        follow=True,
    )

    assert response.status_code == 404
    assert response.content == b'No subscription plan selected.'

@pytest.mark.django_db
def test_subscribe_view_post_preview_200_response(admin_client):
    """Tests post returns 200 response on preview request."""
    plan = create_plan()

    post_data = {
        'action': None,
        'plan_id': plan.id,
    }

    response = admin_client.post(
        reverse('subscriptions_subscribe'),
        post_data,
        follow=True,
    )

    assert response.status_code == 200
