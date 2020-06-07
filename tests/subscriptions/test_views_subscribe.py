"""Tests for the django-flexible-subscriptions UserSubscription views."""
from datetime import datetime
from unittest.mock import patch

import pytest

from django.contrib.auth.models import Group
from django.contrib.messages import get_messages
from django.forms import HiddenInput
from django.urls import reverse
from django.utils import timezone

from subscriptions import models, views, forms


pytestmark = pytest.mark.django_db  # pylint: disable=invalid-name


# SubscribeList Tests
# -----------------------------------------------------------------------------
def test_subscribe_list_template(admin_client, dfs):  # pylint: disable=unused-argument
    """Tests for proper subscribe_list template."""
    # Create plan list
    dfs.plan_list  # pylint: disable=pointless-statement

    response = admin_client.get(reverse('dfs_subscribe_list'))

    assert (
        'subscriptions/subscribe_list.html' in [
            t.name for t in response.templates
        ]
    )


def test_subscribe_list_200_for_anonymous_user(client, dfs):
    """Tests for 200 response for anonymous user"""
    # Create plan list
    dfs.plan_list  # pylint: disable=pointless-statement

    client.force_login(user=dfs.user)
    response = client.get(reverse('dfs_subscribe_list'))

    assert response.status_code == 200


def test_subscribe_list_get_plan_list(admin_client, dfs):
    """Tests list retrieves a single active list"""
    # Create plan list
    dfs.plan_list  # pylint: disable=pointless-statement

    response = admin_client.get(reverse('dfs_subscribe_list'))

    assert response.context['plan_list'] == dfs.plan_list


def test_subscribe_list_get_plan_list_from_multiple(admin_client, dfs):
    """Tests list retrieves a single active list from multiple."""
    # Create plan list
    dfs.plan_list  # pylint: disable=pointless-statement

    # Create a second active plan_list
    models.PlanList.objects.create(active=False)

    response = admin_client.get(reverse('dfs_subscribe_list'))

    assert response.context['plan_list'] == dfs.plan_list


def test_subscribe_list_get_plan_list_with_inactive(admin_client, dfs):
    """Tests list retrieves single active list from multiple + inactive."""
    # Create plan list
    dfs.plan_list  # pylint: disable=pointless-statement

    # Create a second inactive plan_list
    models.PlanList.objects.create(active=False)

    response = admin_client.get(reverse('dfs_subscribe_list'))

    assert response.context['plan_list'] == dfs.plan_list


def test_subscribe_list_get_404_on_no_plans(admin_client):
    """Tests that list returns 404 if no plan lists are created."""
    response = admin_client.get(reverse('dfs_subscribe_list'))

    assert response.status_code == 404
    assert response.content == b'No subscription plans are available'


def test_subscribe_list_get_context_data(admin_client, dfs):  # pylint: disable=unused-argument
    """Tests get_context_data adds plan list and detail to context."""
    # Create plan list and details
    dfs.plan_list  # pylint: disable=pointless-statement

    response = admin_client.get(reverse('dfs_subscribe_list'))

    assert 'plan_list' in response.context
    assert 'details' in response.context


def test_subscribe_list_exclude_plan_with_no_cost(admin_client, dfs):  # pylint: disable=unused-argument
    """Tests that a plan with no cost is excluded."""
    # Create plan list and details
    dfs.plan_list  # pylint: disable=pointless-statement

    # Delete all plan costs
    models.PlanCost.objects.all().delete()

    response = admin_client.get(reverse('dfs_subscribe_list'))

    assert not response.context['details']


def test_subscribe_list_expected_ordering(admin_client, dfs):
    """Tests that details are listed in order."""
    # Create models for view
    plan_list = dfs.plan_list
    details = plan_list.plan_list_details.all().order_by('order')

    response = admin_client.get(reverse('dfs_subscribe_list'))

    assert response.context['details'][0] == details[0]
    assert response.context['details'][1] == details[1]


# SubscribeView Tests
# -----------------------------------------------------------------------------
def test_subscribe_view_redirect_anonymous(client):
    """Tests that anonymous users are redirected to login page."""
    response = client.post(reverse('dfs_subscribe_add'), follow=True)
    redirect_url, redirect_code = response.redirect_chain[-1]

    assert redirect_code == 302
    assert redirect_url == '/accounts/login/?next=/subscribe/add/'


def test_subscribe_view_no_redirect_on_login(client, dfs):
    """Tests that logged in users are not redirected."""
    post_data = {
        'action': '',
        'plan_id': dfs.plan.id,
        'plan_cost': dfs.cost,
    }

    client.force_login(user=dfs.user)
    response = client.post(reverse('dfs_subscribe_add'), post_data, follow=True)

    assert response.status_code == 200


def test_subscribe_view_get_object_404_without_plan(admin_client):
    """Tests get_object returns 404 when plan is missing."""
    post_data = {
        'action': '',
    }
    response = admin_client.post(
        reverse('dfs_subscribe_add'),
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
    success_url = view.get_success_url(
        transaction_id='11111111-1111-4111-a111-111111111111'
    )

    assert success_url == (
        '/subscribe/thank-you/11111111-1111-4111-a111-111111111111/'
    )


def test_subscribe_view_get_405_response(admin_client):
    """Tests that GET returns 405 response."""
    response = admin_client.get(reverse('dfs_subscribe_add'))

    assert response.status_code == 405


def test_subscribe_view_post_preview_200_response(admin_client, dfs):
    """Tests post returns 200 response on preview request."""
    post_data = {
        'action': '',
        'plan_id': dfs.plan.id,
        'plan_cost': dfs.cost,
    }

    response = admin_client.post(
        reverse('dfs_subscribe_add'),
        post_data,
        follow=True,
    )

    assert response.status_code == 200


def test_subscribe_view_post_preview_proper_page(admin_client, dfs):
    """Tests preview POST returns proper details."""
    post_data = {
        'action': 'confirm',
        'plan_id': dfs.plan.id,
        'plan_cost': dfs.cost,
    }

    response = admin_client.post(
        reverse('dfs_subscribe_add'),
        post_data,
        follow=True,
    )

    assert response.context['confirmation'] is False

    templates = [t.name for t in response.templates]
    assert (
        'subscriptions/subscribe_preview.html' in templates
    )


def test_subscribe_view_post_preview_added_context(admin_client, dfs):
    """Tests preview POST adds required forms to context."""
    post_data = {
        'action': '',
        'plan_id': dfs.plan.id,
        'plan_cost': dfs.cost,
    }

    response = admin_client.post(
        reverse('dfs_subscribe_add'),
        post_data,
        follow=True,
    )

    assert 'plan_cost_form' in response.context
    assert isinstance(
        response.context['plan_cost_form'], forms.SubscriptionPlanCostForm
    )
    assert 'payment_form' in response.context
    assert isinstance(response.context['payment_form'], forms.PaymentForm)


def test_subscribe_view_post_preview_progress_to_confirmation(admin_client, dfs):
    """Tests preview POST progresses to confirmation."""
    post_data = {
        'action': 'confirm',
        'plan_id': dfs.plan.id,
        'plan_cost': dfs.cost.id,
        'cardholder_name': 'a',
        'card_number': '1111222233334444',
        'card_expiry_month': '1',
        'card_expiry_year': '2050',
        'card_cvv': '100',
        'address_name': 'a',
        'address_line_1': 'b',
        'address_city': 'c',
        'address_province': 'd',
        'address_country': 'e',
    }

    response = admin_client.post(
        reverse('dfs_subscribe_add'),
        post_data,
        follow=True,
    )

    assert response.context['confirmation'] is True

    templates = [t.name for t in response.templates]
    assert (
        'subscriptions/subscribe_confirmation.html' in templates
    )


def test_subscribe_view_post_preview_to_confirm_invalid(admin_client, dfs):
    """Tests invalid preview to confirmation POST returns to preview."""
    post_data = {
        'action': 'confirm',
        'plan_id': dfs.plan.id,
        'plan_cost': dfs.cost,
        'cardholder_name': '',
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
        reverse('dfs_subscribe_add'),
        post_data,
        follow=True,
    )
    templates = [t.name for t in response.templates]

    assert response.context['confirmation'] is False
    assert 'subscriptions/subscribe_preview.html' in templates


def test_subscribe_view_post_preview_to_confirm_invalid_values(admin_client, dfs):
    """Tests invalid preview that form is repopulated correctly."""
    post_data = {
        'action': 'confirm',
        'plan_id': dfs.plan.id,
        'plan_cost': dfs.cost.id,
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
        reverse('dfs_subscribe_add'),
        post_data,
        follow=True,
    )
    cost_form = response.context['plan_cost_form']
    payment_form = response.context['payment_form']

    assert cost_form.data['plan_cost'] == str(dfs.cost.id)
    assert 'cardholder_name' not in payment_form.data
    assert payment_form.data['card_number'] == '1111222233334444'


def test_subscribe_view_post_confirmation_200_response(admin_client, dfs):
    """Tests post returns 200 response on confirmation request."""
    post_data = {
        'action': 'confirm',
        'plan_id': dfs.plan.id,
        'plan_cost': dfs.cost.id,
    }

    response = admin_client.post(
        reverse('dfs_subscribe_add'),
        post_data,
        follow=True,
    )

    assert response.status_code == 200


def test_subscribe_view_post_confirm_to_process_valid(admin_client, dfs):
    """Tests proper confirmation POST moves to success URL page."""
    post_data = {
        'action': 'process',
        'plan_id': dfs.plan.id,
        'plan_cost': dfs.cost.id,
        'cardholder_name': 'a',
        'card_number': '1111222233334444',
        'card_expiry_month': '1',
        'card_expiry_year': '2050',
        'card_cvv': '100',
        'address_name': 'a',
        'address_line_1': 'b',
        'address_city': 'c',
        'address_province': 'd',
        'address_country': 'e',
    }

    response = admin_client.post(
        reverse('dfs_subscribe_add'),
        post_data,
        follow=True,
    )

    url, _ = response.redirect_chain[-1]

    assert '/subscribe/thank-you' in url


def test_subscribe_view_post_confirm_to_process_invalid(admin_client, dfs):
    """Tests invalid process POST returns to confirmation."""
    post_data = {
        'action': 'process',
        'plan_id': dfs.plan.id,
        'plan_cost': dfs.cost.id,
        'cardholder_name': '',
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
        reverse('dfs_subscribe_add'),
        post_data,
        follow=True,
    )

    assert response.context['confirmation'] is False

    templates = [t.name for t in response.templates]
    assert (
        'subscriptions/subscribe_preview.html' in templates
    )


def test_subscribe_view_post_confirm_to_process_invalid_values(admin_client, dfs):
    """Tests invalid process POST populates proper values in form."""
    post_data = {
        'action': 'process',
        'plan_id': dfs.plan.id,
        'plan_cost': dfs.cost.id,
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
        reverse('dfs_subscribe_add'),
        post_data,
        follow=True,
    )
    cost_form = response.context['plan_cost_form']
    payment_form = response.context['payment_form']

    assert cost_form.data['plan_cost'] == str(dfs.cost.id)
    assert 'cardholder_name' not in payment_form.data
    assert payment_form.data['card_number'] == '1111222233334444'


@patch(
    'subscriptions.views.SubscribeView.process_payment',
    lambda self, **kwargs: False
)
def test_subscribe_view_post_confirm_payment_error(admin_client, dfs):
    """Tests handling of payment error from confirmation POST."""
    post_data = {
        'action': 'process',
        'plan_id': dfs.plan.id,
        'plan_cost': str(dfs.cost.id),
        'cardholder_name': 'a',
        'card_number': '1111222233334444',
        'card_expiry_month': '1',
        'card_expiry_year': '2050',
        'card_cvv': '100',
        'address_name': 'a',
        'address_line_1': 'b',
        'address_city': 'c',
        'address_province': 'd',
        'address_country': 'e',
    }

    response = admin_client.post(
        reverse('dfs_subscribe_add'),
        post_data,
        follow=True,
    )

    templates = [t.name for t in response.templates]
    messages = list(get_messages(response.wsgi_request))

    assert response.context['confirmation'] is True
    assert 'subscriptions/subscribe_confirmation.html' in templates
    assert messages[0].tags == 'error'
    assert messages[0].message == 'Error processing payment'


def test_subscribe_view_post_process_200_response(admin_client, dfs):
    """Tests post returns 200 response on process request."""
    post_data = {
        'action': 'process',
        'plan_id': dfs.plan.id,
        'plan_cost': dfs.cost.id,
    }

    response = admin_client.post(
        reverse('dfs_subscribe_add'),
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


@patch(
    'subscriptions.views.timezone.now', lambda: datetime(2018, 1, 1, 1, 1, 1)
)
def test_subscribe_view_record_transaction_without_date(dfs):
    """Tests handling of record_transaction without providing a date.

        Patching the timezone module to ensure consistent test results.
    """
    transaction_count = models.SubscriptionTransaction.objects.all().count()

    view = views.SubscribeView()
    transaction = view.record_transaction(dfs.subscription)

    assert models.SubscriptionTransaction.objects.all().count() == (
        transaction_count + 1
    )
    assert transaction.date_transaction == datetime(2018, 1, 1, 1, 1, 1)


def test_subscribe_view_record_transaction_with_date(dfs):
    """Tests handling of record_transaction with date provided."""
    transaction_count = models.SubscriptionTransaction.objects.all().count()
    transaction_date = datetime(2018, 1, 2, 1, 1, 1)

    view = views.SubscribeView()
    transaction = view.record_transaction(
        dfs.subscription, transaction_date
    )

    assert models.SubscriptionTransaction.objects.all().count() == (
        transaction_count + 1
    )
    assert transaction.date_transaction == transaction_date


def test_subscribe_view_setup_subscription_user_group(dfs):
    """Tests that user is properly added to group."""
    group, _ = Group.objects.get_or_create(name='test')
    user_count = group.user_set.all().count()
    dfs.plan.group = group

    view = views.SubscribeView()
    view.subscription_plan = dfs.plan
    view.setup_subscription(dfs.user, dfs.cost)

    assert dfs.user in group.user_set.all()
    assert group.user_set.all().count() == user_count + 1


def test_subscribe_view_setup_subscription_user_subscription(dfs):
    """Tests that user subscription entry is setup properly."""
    sub_count = models.UserSubscription.objects.all().count()
    group, _ = Group.objects.get_or_create(name='test')
    dfs.plan.group = group

    view = views.SubscribeView()
    view.subscription_plan = dfs.plan
    view.setup_subscription(dfs.user, dfs.cost)

    assert models.UserSubscription.objects.all().count() == sub_count + 1


def test_subscribe_view_setup_subscription_no_group(dfs):
    """Tests that setup handles subscriptions with no groups."""
    group, _ = Group.objects.get_or_create(name='test')
    user_count = group.user_set.all().count()

    view = views.SubscribeView()
    view.subscription_plan = dfs.plan
    view.setup_subscription(dfs.user, dfs.cost)

    assert dfs.user not in group.user_set.all()
    assert group.user_set.all().count() == user_count


# SubscribeUserListView Tests
# -----------------------------------------------------------------------------
def test_subscribe_user_list_redirect_anonymous(client):
    """Tests that anonymous users are redirected to login page."""
    response = client.get(reverse('dfs_subscribe_user_list'), follow=True)
    redirect_url, redirect_code = response.redirect_chain[-1]

    assert redirect_code == 302
    assert redirect_url == ('/accounts/login/?next=/subscriptions/')


def test_subscribe_user_list_no_redirect_on_login(client, django_user_model):
    """Tests that logged in users are not redirected."""
    django_user_model.objects.create_user(username='a', password='b')
    client.login(username='a', password='b')
    response = client.get(reverse('dfs_subscribe_user_list'), follow=True)

    assert response.status_code == 200


def test_subscribe_user_list_requires_user_owner(client, django_user_model, dfs):
    """Tests that logged in user has ownership of subscription plans."""
    subscription = dfs.subscription
    other_user = django_user_model.objects.create_user(
        username='a', password='b'
    )
    models.UserSubscription.objects.create(user=other_user)

    client.force_login(user=dfs.user)
    response = client.get(reverse('dfs_subscribe_user_list'), follow=True)

    assert response.context['subscriptions'][0] == subscription
    assert models.UserSubscription.objects.all().count() == 2
    assert len(response.context['subscriptions']) == 1


# SubscribeThankYouView Tests
# ----------------------------------------------------------------------------
def test_thank_you_view_redirect_anonymous(client, django_user_model):
    """Tests that anonymous users are redirected to login page."""
    user = django_user_model.objects.create_user(username='a', password='b')
    transaction = models.SubscriptionTransaction.objects.create(
        user=user, amount='1.00', date_transaction=timezone.now()
    )
    response = client.get(
        reverse(
            'dfs_subscribe_thank_you',
            kwargs={'transaction_id': transaction.id},
        ),
        follow=True,
    )
    redirect_url, redirect_code = response.redirect_chain[-1]

    assert redirect_code == 302
    assert redirect_url == (
        '/accounts/login/?next=/subscribe/thank-you/{}/'.format(transaction.id)
    )


def test_thank_you_view_no_redirect_on_login(client, django_user_model):
    """Tests that logged in users are not redirected."""
    user = django_user_model.objects.create_user(username='a', password='b')
    client.login(username='a', password='b')
    transaction = models.SubscriptionTransaction.objects.create(
        user=user, amount='1.00', date_transaction=timezone.now()
    )
    response = client.get(
        reverse(
            'dfs_subscribe_thank_you',
            kwargs={'transaction_id': transaction.id},
        ),
        follow=True,
    )

    assert response.status_code == 200


def test_thank_you_view_returns_object(client, django_user_model):
    """Tests Thank You view properly returns transaction instance."""
    user = django_user_model.objects.create_user(username='a', password='b')
    transaction = models.SubscriptionTransaction.objects.create(
        user=user, amount='1.00', date_transaction=timezone.now()
    )
    client.login(username='a', password='b')
    response = client.get(reverse(
        'dfs_subscribe_thank_you', kwargs={'transaction_id': transaction.id}
    ))

    assert response.status_code == 200


def test_thank_you_view_adds_context(client, django_user_model):
    """Tests that context is properly extended."""
    user = django_user_model.objects.create_user(username='a', password='b')
    transaction = models.SubscriptionTransaction.objects.create(
        user=user, amount='1.00', date_transaction=timezone.now()
    )
    client.login(username='a', password='b')
    response = client.get(reverse(
        'dfs_subscribe_thank_you', kwargs={'transaction_id': transaction.id}
    ))

    assert 'transaction' in response.context
    assert response.context['transaction'] == transaction


# SubscribeCancelView Tests
# -----------------------------------------------------------------------------
def test_cancel_view_redirect_anonymous(client):
    """Tests that anonymous users are redirected to login page."""
    sub_id = models.UserSubscription.objects.create().id
    response = client.get(
        reverse('dfs_subscribe_cancel', kwargs={'subscription_id': sub_id}),
        follow=True)
    redirect_url, redirect_code = response.redirect_chain[-1]

    assert redirect_code == 302
    assert redirect_url == (
        '/accounts/login/?next=/subscribe/cancel/{}/'.format(sub_id))


def test_cancel_view_no_redirect_on_login(client, dfs):
    """Tests that logged in users are not redirected."""
    subscription = dfs.subscription
    subscription_id = subscription.id

    client.force_login(dfs.user)
    response = client.get(
        reverse(
            'dfs_subscribe_cancel',
            kwargs={'subscription_id': subscription_id},
        ),
        follow=True,
    )

    assert response.status_code == 200


def test_cancel_view_get_success_url():
    """Tests that get_success_url works properly."""
    view = views.SubscribeCancelView()
    assert view.get_success_url() == '/subscriptions/'


def test_cancel_post_updates_instance(client, dfs):
    """Tests that POST request properly updates subscription instance."""
    subscription = dfs.subscription
    subscription_id = subscription.id

    client.force_login(dfs.user)
    response = client.post(
        reverse(
            'dfs_subscribe_cancel', kwargs={'subscription_id': subscription_id}
        ),
        follow=True
    )

    subscription = models.UserSubscription.objects.get(id=subscription_id)
    messages = [message for message in get_messages(response.wsgi_request)]

    assert subscription.date_billing_end == datetime(2018, 2, 1, 1, 1, 1)
    assert subscription.date_billing_next is None
    assert messages[0].tags == 'success'
    assert messages[0].message == 'Subscription successfully cancelled'


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
