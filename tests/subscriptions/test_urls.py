"""Tests for the Helcim URLs."""
import pytest

from django.urls import reverse

from subscriptions import models

@pytest.mark.django_db
def test_tag_list_exists_at_desired_location(admin_client):
    """Tests that tag list URL name works."""
    response = admin_client.get(reverse('subscriptions_tag_list'))

    assert response.status_code == 200

@pytest.mark.django_db
def test_tag_list_exists_at_desired_url(admin_client):
    """Tests that tag list URL works."""
    response = admin_client.get('/tags/')

    assert response.status_code == 200

@pytest.mark.django_db
def test_tag_create_exists_at_desired_location(admin_client):
    """Tests that tag create URL name works."""
    response = admin_client.get(reverse('subscriptions_tag_create'))

    assert response.status_code == 200

@pytest.mark.django_db
def test_tag_create_exists_at_desired_url(admin_client):
    """Tests that tag create URL works."""
    response = admin_client.get('/tags/create/')

    assert response.status_code == 200

@pytest.mark.django_db
def test_tag_update_exists_at_desired_location(admin_client):
    """Tests that tag update URL name works."""
    tag = models.PlanTag.objects.create(tag='test')
    response = admin_client.get(reverse(
        'subscriptions_tag_update',
        kwargs={'tag_id': tag.id}
    ))

    assert response.status_code == 200

@pytest.mark.django_db
def test_tag_update_exists_at_desired_url(admin_client):
    """Tests that tag update URL works."""
    tag = models.PlanTag.objects.create(tag='test')
    response = admin_client.get('/tags/{}/'.format(tag.id))

    assert response.status_code == 200

@pytest.mark.django_db
def test_tag_delete_exists_at_desired_location(admin_client):
    """Tests that tag delete URL name works."""
    tag = models.PlanTag.objects.create(tag='test')
    response = admin_client.get(reverse(
        'subscriptions_tag_delete',
        kwargs={'tag_id': tag.id}
    ))

    assert response.status_code == 200

@pytest.mark.django_db
def test_tag_delete_exists_at_desired_url(admin_client):
    """Tests that tag delete URL works."""
    tag = models.PlanTag.objects.create(tag='test')
    response = admin_client.get('/tags/{}/delete/'.format(tag.id))

    assert response.status_code == 200

@pytest.mark.django_db
def test_plan_list_exists_at_desired_location(admin_client):
    """Tests that plan list URL name works."""
    response = admin_client.get(reverse('subscriptions_plan_list'))

    assert response.status_code == 200

@pytest.mark.django_db
def test_plan_list_exists_at_desired_url(admin_client):
    """Tests that plan list URL works."""
    response = admin_client.get('/plans/')

    assert response.status_code == 200

@pytest.mark.django_db
def test_plan_create_exists_at_desired_location(admin_client):
    """Tests that plan create URL name works."""
    response = admin_client.get(reverse('subscriptions_plan_create'))

    assert response.status_code == 200

@pytest.mark.django_db
def test_plan_create_exists_at_desired_url(admin_client):
    """Tests that plan create URL works."""
    response = admin_client.get('/plans/create/')

    assert response.status_code == 200

@pytest.mark.django_db
def test_plan_update_exists_at_desired_location(admin_client):
    """Tests that plan update URL name works."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='a', plan_description='b'
    )
    response = admin_client.get(
        reverse('subscriptions_plan_update', kwargs={'plan_id': plan.id})
    )

    assert response.status_code == 200

@pytest.mark.django_db
def test_plan_updated_exists_at_desired_url(admin_client):
    """Tests that plan update URL works."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='a', plan_description='b'
    )
    response = admin_client.get('/plans/{}/'.format(plan.id))

    assert response.status_code == 200

@pytest.mark.django_db
def test_plan_delete_exists_at_desired_location(admin_client):
    """Tests that plan delete URL name works."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='a', plan_description='b'
    )
    response = admin_client.get(
        reverse('subscriptions_plan_delete', kwargs={'plan_id': plan.id})
    )

    assert response.status_code == 200

@pytest.mark.django_db
def test_plan_delete_exists_at_desired_url(admin_client):
    """Tests that plan delete URL works."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='a', plan_description='b'
    )
    response = admin_client.get('/plans/{}/delete/'.format(plan.id))

    assert response.status_code == 200

@pytest.mark.django_db
def test_subscriptions_subscribe_exists_at_desired_location(admin_client):
    """Tests that subscription subscribe URL name works."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='a', plan_description='b'
    )
    response = admin_client.post(
        reverse('subscriptions_subscribe'), {'plan_id': plan.id}
    )

    assert response.status_code == 200

@pytest.mark.django_db
def test_subscription_subscribe_exists_at_desired_url(admin_client):
    """Tests that subscription subscribe URL works."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='a', plan_description='b'
    )
    response = admin_client.post('/subscribe/', {'plan_id': plan.id})

    assert response.status_code == 200

@pytest.mark.django_db
def test_subscription_list_exists_at_desired_location(admin_client):
    """Tests that subscription list URL name works."""
    response = admin_client.get(reverse('subscriptions_subscription_list'))

    assert response.status_code == 200

@pytest.mark.django_db
def test_subscription_list_exists_at_desired_url(admin_client):
    """Tests that subscription list URL works."""
    response = admin_client.get('/subscriptions/')

    assert response.status_code == 200

@pytest.mark.django_db
def test_subscription_create_exists_at_desired_location(admin_client):
    """Tests that subscription create URL name works."""
    response = admin_client.get(reverse('subscriptions_subscription_create'))

    assert response.status_code == 200

@pytest.mark.django_db
def test_subscription_create_exists_at_desired_url(admin_client):
    """Tests that subscription create URL works."""
    response = admin_client.get('/subscriptions/create/')

    assert response.status_code == 200

@pytest.mark.django_db
def test_subscription_update_exists_at_desired_location(admin_client):
    """Tests that subscription update URL name works."""
    subscription = models.UserSubscription.objects.create()
    response = admin_client.get(reverse(
        'subscriptions_subscription_update',
        kwargs={'subscription_id': subscription.id}
    ))

    assert response.status_code == 200

@pytest.mark.django_db
def test_subscription_updated_exists_at_desired_url(admin_client):
    """Tests that subscription update URL works."""
    subscription = models.UserSubscription.objects.create()

    response = admin_client.get('/subscriptions/{}/'.format(subscription.id))

    assert response.status_code == 200

@pytest.mark.django_db
def test_subscription_delete_exists_at_desired_location(admin_client):
    """Tests that subscription delete URL name works."""
    subscription = models.UserSubscription.objects.create()

    response = admin_client.get(reverse(
        'subscriptions_subscription_delete',
        kwargs={'subscription_id': subscription.id}
    ))

    assert response.status_code == 200

@pytest.mark.django_db
def test_subscription_delete_exists_at_desired_url(admin_client):
    """Tests that subscription delete URL works."""
    subscription = models.UserSubscription.objects.create()

    response = admin_client.get(
        '/subscriptions/{}/delete/'.format(subscription.id)
    )

    assert response.status_code == 200

@pytest.mark.django_db
def test_transaction_list_exists_at_desired_location(admin_client):
    """Tests that transaction list URL name works."""
    response = admin_client.get(reverse('subscriptions_transaction_list'))

    assert response.status_code == 200

@pytest.mark.django_db
def test_transaction_list_exists_at_desired_url(admin_client):
    """Tests that transaction list URL works."""
    response = admin_client.get('/transactions/')

    assert response.status_code == 200

@pytest.mark.django_db
def test_transaction_detail_exists_at_desired_location(admin_client):
    """Tests that transaction detail URL name works."""
    transaction = models.SubscriptionTransaction.objects.create()

    response = admin_client.get(reverse(
        'subscriptions_transaction_detail',
        kwargs={'transaction_id': transaction.id}
    ))

    assert response.status_code == 200

@pytest.mark.django_db
def test_transaction_detail_exists_at_desired_url(admin_client):
    """Tests that transaction detail URL works."""
    transaction = models.SubscriptionTransaction.objects.create()

    response = admin_client.get(
        '/transactions/{}/'.format(transaction.id)
    )

    assert response.status_code == 200

@pytest.mark.django_db
def test_thank_you_exists_at_desired_location(admin_client):
    """Tests that thank you page URL name works."""
    response = admin_client.get(reverse('subscriptions_thank_you'))

    assert response.status_code == 200

@pytest.mark.django_db
def test_thank_you_exists_at_desired_url(admin_client):
    """Tests that thank you page URL works."""
    response = admin_client.get('/thank-you/')

    assert response.status_code == 200

@pytest.mark.django_db
def test_susbscription_cancel_exists_at_desired_location(admin_client):
    """Tests that subscription cancel URL name works."""
    subscription = models.UserSubscription.objects.create()
    response = admin_client.get(reverse(
        'subscriptions_cancel', kwargs={'subscription_id': subscription.id}
    ))

    assert response.status_code == 200

@pytest.mark.django_db
def test_subscription_cancel_exists_at_desired_url(admin_client):
    """Tests that subscription cancel URL works."""
    subscription = models.UserSubscription.objects.create()
    response = admin_client.get('/cancel/{}/'.format(subscription.id))

    assert response.status_code == 200

@pytest.mark.django_db
def test_dashboard_exists_at_desired_location(admin_client):
    """Tests that dashboard URL name works."""
    response = admin_client.get(reverse('subscriptions_dashboard'))

    assert response.status_code == 200

@pytest.mark.django_db
def test_dashboard_exists_at_desired_url(admin_client):
    """Tests that dashboard URL works."""
    response = admin_client.get('/')

    assert response.status_code == 200
