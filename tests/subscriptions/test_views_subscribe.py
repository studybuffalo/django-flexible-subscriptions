"""Tests for the django-flexible-subscriptions UserSubscription views."""
from datetime import datetime
from unittest.mock import patch

import pytest

from django.contrib.auth.models import Group
from django.contrib.messages import get_messages
from django.forms import HiddenInput
from django.urls import reverse

from subscriptions import models, views, forms


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


# SubscribeView Tests
# -----------------------------------------------------------------------------
def test_subscribe_view_redirect_anonymous(client):
    """Tests that anonymous users are redirected to login page."""
    response = client.post(reverse('dfs_subscribe'), follow=True)
    redirect_url, redirect_code = response.redirect_chain[-1]

    assert redirect_code == 302
    assert redirect_url == '/accounts/login/?next=/subscribe/'

def test_subscribe_view_no_redirect_on_login(client, django_user_model):
    """Tests that logged in users are not redirected."""
    plan = create_plan()
    post_data = {'action': None, 'plan_id': plan.id}

    django_user_model.objects.create_user(username='a', password='b')
    client.login(username='a', password='b')
    response = client.post(reverse('dfs_subscribe'), post_data, follow=True)

    assert response.status_code == 200

@pytest.mark.django_db
def test_subscribe_view_get_object_404_without_plan(admin_client):
    """Tests get_object returns 404 when plan is missing."""
    post_data = {
        'action': None,
    }
    response = admin_client.post(
        reverse('dfs_subscribe'),
        post_data,
        follow=True,
    )

    assert response.status_code == 404

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
def test_subscribe_view_get_405_response(admin_client):
    """Tests that GET returns 405 response."""
    response = admin_client.get(reverse('dfs_subscribe'))

    assert response.status_code == 405

@pytest.mark.django_db
def test_subscribe_view_post_preview_200_response(admin_client):
    """Tests post returns 200 response on preview request."""
    plan = create_plan()

    post_data = {
        'action': None,
        'plan_id': plan.id,
    }

    response = admin_client.post(
        reverse('dfs_subscribe'),
        post_data,
        follow=True,
    )

    assert response.status_code == 200

@pytest.mark.django_db
def test_subscribe_view_post_preview_proper_page(admin_client):
    """Tests preview POST returns proper details."""
    plan = create_plan()

    post_data = {
        'action': 'confirm',
        'plan_id': plan.id,
    }

    response = admin_client.post(
        reverse('dfs_subscribe'),
        post_data,
        follow=True,
    )

    assert response.context['confirmation'] is False

    templates = [t.name for t in response.templates]
    assert (
        'subscriptions/subscribe_preview.html' in templates
    )

@pytest.mark.django_db
def test_subscribe_view_post_preview_added_context(admin_client):
    """Tests preview POST adds required forms to context."""
    plan = create_plan()
    post_data = {
        'action': None,
        'plan_id': plan.id,
    }

    response = admin_client.post(
        reverse('dfs_subscribe'),
        post_data,
        follow=True,
    )

    assert 'plan_cost_form' in response.context
    assert isinstance(
        response.context['plan_cost_form'], forms.SubscriptionPlanCostForm
    )
    assert 'payment_form' in response.context
    assert isinstance(response.context['payment_form'], forms.PaymentForm)

@pytest.mark.django_db
def test_subscribe_view_post_preview_progress_to_confirmation(admin_client):
    """Tests preview POST progresses to confirmation."""
    plan = create_plan()
    cost = create_cost(plan=plan)
    post_data = {
        'action': 'confirm',
        'plan_id': plan.id,
        'plan_cost': cost.id,
        'cardholder_name': 'a',
        'card_number': '1111222233334444',
        'card_expiry_month': '01',
        'card_expiry_year': '20',
        'card_cvv': '100',
        'address_name': 'a',
        'address_line_1': 'b',
        'address_city': 'c',
        'address_province': 'd',
        'address_country': 'e',
    }

    response = admin_client.post(
        reverse('dfs_subscribe'),
        post_data,
        follow=True,
    )

    assert response.context['confirmation'] is True

    templates = [t.name for t in response.templates]
    assert (
        'subscriptions/subscribe_confirmation.html' in templates
    )

@pytest.mark.django_db
def test_subscribe_view_post_preview_to_confirm_invalid(admin_client):
    """Tests invalid preview to confirmation POST returns to preview."""
    plan = create_plan()
    post_data = {
        'action': 'confirm',
        'plan_id': plan.id,
        'plan_cost': None,
        'cardholder_name': 'a',
        'card_number': '1111222233334444',
        'card_expiry_month': '01',
        'card_expiry_year': '20',
        'card_cvv': '100',
        'address_name': 'a',
        'address_line_1': 'b',
        'address_city': 'c',
        'address_province': 'd',
        'address_country': 'e',
    }

    response = admin_client.post(
        reverse('dfs_subscribe'),
        post_data,
        follow=True,
    )
    templates = [t.name for t in response.templates]

    assert response.context['confirmation'] is False
    assert 'subscriptions/subscribe_preview.html' in templates

@pytest.mark.django_db
def test_subscribe_view_post_preview_to_confirm_invalid_values(admin_client):
    """Tests invalid preview that form is repopulated correctly."""
    plan = create_plan()
    cost = create_cost(plan=plan)
    post_data = {
        'action': 'confirm',
        'plan_id': plan.id,
        'plan_cost': cost.id,
        'card_number': '1111222233334444',
        'card_expiry_month': '01',
        'card_expiry_year': '20',
        'card_cvv': '100',
        'address_name': 'a',
        'address_line_1': 'b',
        'address_city': 'c',
        'address_province': 'd',
        'address_country': 'e',
    }

    response = admin_client.post(
        reverse('dfs_subscribe'),
        post_data,
        follow=True,
    )
    cost_form = response.context['plan_cost_form']
    payment_form = response.context['payment_form']

    assert cost_form.data['plan_cost'] == str(cost.id)
    assert 'cardholder_name' not in payment_form.data
    assert payment_form.data['card_number'] == '1111222233334444'

@pytest.mark.django_db
def test_subscribe_view_post_confirmation_200_response(admin_client):
    """Tests post returns 200 response on confirmation request."""
    plan = create_plan()

    post_data = {
        'action': 'confirm',
        'plan_id': plan.id,
    }

    response = admin_client.post(
        reverse('dfs_subscribe'),
        post_data,
        follow=True,
    )

    assert response.status_code == 200

@pytest.mark.django_db
def test_subscribe_view_post_confirm_to_process_valid(admin_client):
    """Tests proper confirmation POST moves to process page."""
    plan = create_plan()
    cost = create_cost(plan=plan)
    post_data = {
        'action': 'process',
        'plan_id': plan.id,
        'plan_cost': cost.id,
        'cardholder_name': 'a',
        'card_number': '1111222233334444',
        'card_expiry_month': '01',
        'card_expiry_year': '20',
        'card_cvv': '100',
        'address_name': 'a',
        'address_line_1': 'b',
        'address_city': 'c',
        'address_province': 'd',
        'address_country': 'e',
    }

    response = admin_client.post(
        reverse('dfs_subscribe'),
        post_data,
        follow=True,
    )

    url, _ = response.redirect_chain[-1]

    assert url == '/'

@pytest.mark.django_db
def test_subscribe_view_post_confirm_to_process_invalid(admin_client):
    """Tests invalid process POST returns to confirmation."""
    plan = create_plan()
    post_data = {
        'action': 'process',
        'plan_id': plan.id,
        'plan_cost': None,
        'cardholder_name': 'a',
        'card_number': '1111222233334444',
        'card_expiry_month': '01',
        'card_expiry_year': '20',
        'card_cvv': '100',
        'address_name': 'a',
        'address_line_1': 'b',
        'address_city': 'c',
        'address_province': 'd',
        'address_country': 'e',
    }

    response = admin_client.post(
        reverse('dfs_subscribe'),
        post_data,
        follow=True,
    )

    assert response.context['confirmation'] is True

    templates = [t.name for t in response.templates]
    assert (
        'subscriptions/subscribe_confirmation.html' in templates
    )

@pytest.mark.django_db
def test_subscribe_view_post_confirm_to_process_invalid_values(admin_client):
    """Tests invalid process POST populates proper values in form."""
    plan = create_plan()
    cost = create_cost(plan=plan)
    post_data = {
        'action': 'process',
        'plan_id': plan.id,
        'plan_cost': cost.id,
        'card_number': '1111222233334444',
        'card_expiry_month': '01',
        'card_expiry_year': '20',
        'card_cvv': '100',
        'address_name': 'a',
        'address_line_1': 'b',
        'address_city': 'c',
        'address_province': 'd',
        'address_country': 'e',
    }

    response = admin_client.post(
        reverse('dfs_subscribe'),
        post_data,
        follow=True,
    )
    cost_form = response.context['plan_cost_form']
    payment_form = response.context['payment_form']

    assert cost_form.data['plan_cost'] == str(cost.id)
    assert 'cardholder_name' not in payment_form.data
    assert payment_form.data['card_number'] == '1111222233334444'

@patch('subscriptions.views.SubscribeView.process_payment', lambda x, y: False)
@pytest.mark.django_db
def test_subscribe_view_post_confirm_payment_error(admin_client):
    """Tests handling of payment error from confirmation POST."""
    plan = create_plan()
    cost = create_cost(plan=plan)
    post_data = {
        'action': 'process',
        'plan_id': plan.id,
        'plan_cost': cost.id,
        'cardholder_name': 'a',
        'card_number': '1111222233334444',
        'card_expiry_month': '01',
        'card_expiry_year': '20',
        'card_cvv': '100',
        'address_name': 'a',
        'address_line_1': 'b',
        'address_city': 'c',
        'address_province': 'd',
        'address_country': 'e',
    }

    response = admin_client.post(
        reverse('dfs_subscribe'),
        post_data,
        follow=True,
    )

    templates = [t.name for t in response.templates]
    messages = list(get_messages(response.wsgi_request))

    assert response.context['confirmation'] is True
    assert 'subscriptions/subscribe_confirmation.html' in templates
    assert messages[0].tags == 'error'
    assert messages[0].message == 'Error processing payment'

@pytest.mark.django_db
def test_subscribe_view_post_process_200_response(admin_client):
    """Tests post returns 200 response on process request."""
    plan = create_plan()

    post_data = {
        'action': 'process',
        'plan_id': plan.id,
    }

    response = admin_client.post(
        reverse('dfs_subscribe'),
        post_data,
        follow=True,
    )

    assert response.status_code == 200

def test_subscribe_view_hide_form():
    """Tests that hide_form converts all widgets to hidden inputs."""
    view = views.SubscribeView()
    form = forms.PaymentForm()
    hidden_form = view.hide_form(form)

    for _, field in hidden_form.fields.items():
        assert isinstance(field.widget, HiddenInput)

@pytest.mark.django_db
def test_subscribe_view_setup_subscription_user_group(django_user_model):
    """Tests that user is properly added to group."""
    user = django_user_model.objects.create_user(username='a', password='b')
    group, _ = Group.objects.get_or_create(name='test')
    user_count = group.user_set.all().count()

    plan = create_plan()
    plan.group = group
    cost = create_cost(plan=plan)

    view = views.SubscribeView()
    view.subscription_plan = plan
    view.setup_subscription(user, cost.id)

    assert user in group.user_set.all()
    assert group.user_set.all().count() == user_count + 1

@pytest.mark.django_db
def test_subscribe_view_setup_subscription_user_subscription(django_user_model):
    """Tests that user subscription entry is setup properly."""
    sub_count = models.UserSubscription.objects.all().count()

    user = django_user_model.objects.create_user(username='a', password='b')
    group, _ = Group.objects.get_or_create(name='test')

    plan = create_plan()
    plan.group = group
    cost = create_cost(plan=plan)

    view = views.SubscribeView()
    view.subscription_plan = plan
    view.setup_subscription(user, cost.id)

    assert models.UserSubscription.objects.all().count() == sub_count + 1

@pytest.mark.django_db
def test_subscribe_view_setup_subscription_no_group(django_user_model):
    """Tests that setup handles subscriptions with no groups."""
    user = django_user_model.objects.create_user(username='a', password='b')
    group, _ = Group.objects.get_or_create(name='test')
    user_count = group.user_set.all().count()

    plan = create_plan()
    cost = create_cost(plan=plan)

    view = views.SubscribeView()
    view.subscription_plan = plan
    view.setup_subscription(user, cost.id)

    assert user not in group.user_set.all()
    assert group.user_set.all().count() == user_count


# SubscribeThankYouView Tests
# ----------------------------------------------------------------------------
def test_thank_you_view_redirect_anonymous(client):
    """Tests that anonymous users are redirected to login page."""
    response = client.get(reverse('dfs_subscribe_thank_you'), follow=True)
    redirect_url, redirect_code = response.redirect_chain[-1]

    assert redirect_code == 302
    assert redirect_url == '/accounts/login/?next=/thank-you/'

def test_thank_you_view_no_redirect_on_login(client, django_user_model):
    """Tests that logged in users are not redirected."""
    django_user_model.objects.create_user(username='a', password='b')
    client.login(username='a', password='b')
    response = client.get(reverse('dfs_subscribe_thank_you'), follow=True)

    assert response.status_code == 200

@pytest.mark.django_db
def test_thank_you_view_returns_object(admin_client):
    """Tests Thank You view properly returns transaction instance."""
    transaction = models.SubscriptionTransaction.objects.create(amount='1.00')

    response = admin_client.get('{}?transaction_id={}'.format(
        reverse('dfs_subscribe_thank_you'), transaction.id
    ))

    assert response.status_code == 200

def test_thank_you_view_adds_context(admin_client):
    """Tests that context is properly extended."""
    transaction = models.SubscriptionTransaction.objects.create(amount='1.00')

    response = admin_client.get('{}?transaction_id={}'.format(
        reverse('dfs_subscribe_thank_you'), transaction.id
    ))
    assert 'transaction' in response.context
    assert response.context['transaction'] == transaction


# SubscribeCancelView Tests
# -----------------------------------------------------------------------------
@pytest.mark.django_db
def test_cancel_view_redirect_anonymous(client):
    """Tests that anonymous users are redirected to login page."""
    sub_id = models.UserSubscription.objects.create().id
    response = client.get(
        reverse('dfs_subscribe_cancel', kwargs={'subscription_id': sub_id}),
        follow=True)
    redirect_url, redirect_code = response.redirect_chain[-1]

    assert redirect_code == 302
    assert redirect_url == '/accounts/login/?next=/cancel/{}/'.format(sub_id)

@pytest.mark.django_db
def test_cancel_view_no_redirect_on_login(client, django_user_model):
    """Tests that logged in users are not redirected."""
    user = django_user_model.objects.create_user(username='a', password='b')
    sub_id = models.UserSubscription.objects.create(user=user).id
    client.login(username='a', password='b')
    response = client.get(
        reverse('dfs_subscribe_cancel', kwargs={'subscription_id': sub_id}),
        follow=True)

    assert response.status_code == 200

def test_cancel_view_get_success_url():
    """Tests that get_success_url works properly."""
    view = views.SubscribeView()
    assert view.get_success_url() == '/'

@pytest.mark.django_db
def test_cancel_post_updates_instance(client, django_user_model):
    """Tests that POST request properly updates subscription instance."""
    user = django_user_model.objects.create_user(username='a', password='b')
    subscription = models.UserSubscription.objects.create(
        user=user,
        date_billing_start=datetime(2018, 1, 1),
        date_billing_end=None,
        date_billing_last=datetime(2018, 11, 1),
        date_billing_next=datetime(2018, 12, 1),
    )
    subscription_id = subscription.id
    client.login(username='a', password='b')
    response = client.post(
        reverse(
            'dfs_subscribe_cancel', kwargs={'subscription_id': subscription_id}
        ),
        follow=True
    )

    subscription = models.UserSubscription.objects.get(id=subscription_id)
    messages = [message for message in get_messages(response.wsgi_request)]

    assert subscription.date_billing_end == datetime(2018, 12, 1)
    assert subscription.date_billing_next is None
    assert messages[0].tags == 'success'
    assert messages[0].message == 'Subscription successfully cancelled'

@pytest.mark.django_db
def test_cancel_requires_user_owner(client, django_user_model):
    """Tests that logged in user has ownership of subscription plan."""
    django_user_model.objects.create_user(username='a', password='b')
    user_2 = django_user_model.objects.create_user(username='c', password='d')
    sub_id = models.UserSubscription.objects.create(user=user_2).id
    client.login(username='a', password='b')
    response = client.get(
        reverse('dfs_subscribe_cancel', kwargs={'subscription_id': sub_id}),
        follow=True)

    assert response.status_code == 404
