"""Tests for the Helcim URLs."""
import pytest

from django.urls import reverse
from django.utils import timezone

from subscriptions import models


pytestmark = pytest.mark.django_db  # pylint: disable=invalid-name

def test_subscribe_add_exists_at_desired_location(admin_client):
    """Tests that subscribe add URL name works."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='a', plan_description='b'
    )
    cost = models.PlanCost.objects.create(plan=plan, cost='1.00')
    response = admin_client.post(
        reverse('dfs_subscribe_add'), {'plan_id': plan.id, 'plan_cost': cost}
    )

    assert response.status_code == 200

def test_subscribe_add_exists_at_desired_url(admin_client):
    """Tests that subscribe add URL works."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='a', plan_description='b'
    )
    cost = models.PlanCost.objects.create(plan=plan, cost='1.00')
    response = admin_client.post(
        '/subscribe/add/', {'plan_id': plan.id, 'plan_cost': cost}
    )

    assert response.status_code == 200

def test_thank_you_exists_at_desired_location(admin_client, django_user_model):
    """Tests that thank you page URL name works."""
    user = django_user_model.objects.create_user(username='a', password='b')
    transaction = models.SubscriptionTransaction.objects.create(
        user=user, amount='1.00', date_transaction=timezone.now()
    )

    response = admin_client.get(reverse(
        'dfs_subscribe_thank_you', kwargs={'transaction_id': transaction.id}
    ))

    assert response.status_code == 200

def test_thank_you_exists_at_desired_url(admin_client, django_user_model):
    """Tests that thank you page URL works."""
    user = django_user_model.objects.create_user(username='a', password='b')
    transaction = models.SubscriptionTransaction.objects.create(
        user=user, amount='1.00', date_transaction=timezone.now()
    )

    response = admin_client.get(
        '/subscribe/thank-you/{}/'.format(transaction.id)
    )

    assert response.status_code == 200

def test_cancel_exists_at_desired_location(client, dfs):
    """Tests that subscription cancel URL name works."""
    subscription = dfs.subscription

    client.force_login(user=dfs.user)
    response = client.get(reverse(
        'dfs_subscribe_cancel', kwargs={'subscription_id': subscription.id}))

    assert response.status_code == 200

def test_cancel_exists_at_desired_url(client, dfs):
    """Tests that subscription cancel URL works."""
    subscription = dfs.subscription

    client.force_login(user=dfs.user)
    response = client.get('/subscribe/cancel/{}/'.format(subscription.id))

    assert response.status_code == 200

def test_subscribe_user_list_exists_at_desired_location(admin_client):
    """Tests that subscribe list URL name works."""
    response = admin_client.get(reverse('dfs_subscribe_user_list'))

    assert response.status_code == 200

def test_subscribe_user_list_exists_at_desired_url(admin_client):
    """Tests that subscription cancel URL works."""
    response = admin_client.get('/subscriptions/')

    assert response.status_code == 200

def test_tag_list_exists_at_desired_location(admin_client):
    """Tests that tag list URL name works."""
    response = admin_client.get(reverse('dfs_tag_list'))

    assert response.status_code == 200

def test_tag_list_exists_at_desired_url(admin_client):
    """Tests that tag list URL works."""
    response = admin_client.get('/dfs/tags/')

    assert response.status_code == 200

def test_tag_create_exists_at_desired_location(admin_client):
    """Tests that tag create URL name works."""
    response = admin_client.get(reverse('dfs_tag_create'))

    assert response.status_code == 200

def test_tag_create_exists_at_desired_url(admin_client):
    """Tests that tag create URL works."""
    response = admin_client.get('/dfs/tags/create/')

    assert response.status_code == 200

def test_tag_update_exists_at_desired_location(admin_client):
    """Tests that tag update URL name works."""
    tag = models.PlanTag.objects.create(tag='test')
    response = admin_client.get(reverse(
        'dfs_tag_update',
        kwargs={'tag_id': tag.id}
    ))

    assert response.status_code == 200

def test_tag_update_exists_at_desired_url(admin_client):
    """Tests that tag update URL works."""
    tag = models.PlanTag.objects.create(tag='test')
    response = admin_client.get('/dfs/tags/{}/'.format(tag.id))

    assert response.status_code == 200

def test_tag_delete_exists_at_desired_location(admin_client):
    """Tests that tag delete URL name works."""
    tag = models.PlanTag.objects.create(tag='test')
    response = admin_client.get(reverse(
        'dfs_tag_delete',
        kwargs={'tag_id': tag.id}
    ))

    assert response.status_code == 200

def test_tag_delete_exists_at_desired_url(admin_client):
    """Tests that tag delete URL works."""
    tag = models.PlanTag.objects.create(tag='test')
    response = admin_client.get('/dfs/tags/{}/delete/'.format(tag.id))

    assert response.status_code == 200

def test_plan_list_exists_at_desired_location(admin_client):
    """Tests that plan list URL name works."""
    response = admin_client.get(reverse('dfs_plan_list'))

    assert response.status_code == 200

def test_plan_list_exists_at_desired_url(admin_client):
    """Tests that plan list URL works."""
    response = admin_client.get('/dfs/plans/')

    assert response.status_code == 200

def test_plan_create_exists_at_desired_location(admin_client):
    """Tests that plan create URL name works."""
    response = admin_client.get(reverse('dfs_plan_create'))

    assert response.status_code == 200

def test_plan_create_exists_at_desired_url(admin_client):
    """Tests that plan create URL works."""
    response = admin_client.get('/dfs/plans/create/')

    assert response.status_code == 200

def test_plan_update_exists_at_desired_location(admin_client):
    """Tests that plan update URL name works."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='a', plan_description='b'
    )
    response = admin_client.get(
        reverse('dfs_plan_update', kwargs={'plan_id': plan.id})
    )

    assert response.status_code == 200

def test_plan_updated_exists_at_desired_url(admin_client):
    """Tests that plan update URL works."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='a', plan_description='b'
    )
    response = admin_client.get('/dfs/plans/{}/'.format(plan.id))

    assert response.status_code == 200

def test_plan_delete_exists_at_desired_location(admin_client):
    """Tests that plan delete URL name works."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='a', plan_description='b'
    )
    response = admin_client.get(
        reverse('dfs_plan_delete', kwargs={'plan_id': plan.id})
    )

    assert response.status_code == 200

def test_plan_delete_exists_at_desired_url(admin_client):
    """Tests that plan delete URL works."""
    plan = models.SubscriptionPlan.objects.create(
        plan_name='a', plan_description='b'
    )
    response = admin_client.get('/dfs/plans/{}/delete/'.format(plan.id))

    assert response.status_code == 200

def test_subscription_list_exists_at_desired_location(admin_client):
    """Tests that subscription list URL name works."""
    response = admin_client.get(reverse('dfs_subscription_list'))

    assert response.status_code == 200

def test_subscription_list_exists_at_desired_url(admin_client):
    """Tests that subscription list URL works."""
    response = admin_client.get('/dfs/subscriptions/')

    assert response.status_code == 200

def test_subscription_create_exists_at_desired_location(admin_client):
    """Tests that subscription create URL name works."""
    response = admin_client.get(reverse('dfs_subscription_create'))

    assert response.status_code == 200

def test_subscription_create_exists_at_desired_url(admin_client):
    """Tests that subscription create URL works."""
    response = admin_client.get('/dfs/subscriptions/create/')

    assert response.status_code == 200

def test_subscription_update_exists_at_desired_location(admin_client):
    """Tests that subscription update URL name works."""
    subscription = models.UserSubscription.objects.create()
    response = admin_client.get(reverse(
        'dfs_subscription_update',
        kwargs={'subscription_id': subscription.id}
    ))

    assert response.status_code == 200

def test_subscription_updated_exists_at_desired_url(admin_client):
    """Tests that subscription update URL works."""
    subscription = models.UserSubscription.objects.create()

    response = admin_client.get(
        '/dfs/subscriptions/{}/'.format(subscription.id))

    assert response.status_code == 200

def test_subscription_delete_exists_at_desired_location(admin_client):
    """Tests that subscription delete URL name works."""
    subscription = models.UserSubscription.objects.create()

    response = admin_client.get(reverse(
        'dfs_subscription_delete',
        kwargs={'subscription_id': subscription.id}
    ))

    assert response.status_code == 200

def test_subscription_delete_exists_at_desired_url(admin_client):
    """Tests that subscription delete URL works."""
    subscription = models.UserSubscription.objects.create()

    response = admin_client.get(
        '/dfs/subscriptions/{}/delete/'.format(subscription.id)
    )

    assert response.status_code == 200

def test_transaction_list_exists_at_desired_location(admin_client):
    """Tests that transaction list URL name works."""
    response = admin_client.get(reverse('dfs_transaction_list'))

    assert response.status_code == 200

def test_transaction_list_exists_at_desired_url(admin_client):
    """Tests that transaction list URL works."""
    response = admin_client.get('/dfs/transactions/')

    assert response.status_code == 200

def test_transaction_detail_exists_at_desired_location(admin_client):
    """Tests that transaction detail URL name works."""
    transaction = models.SubscriptionTransaction.objects.create(
        date_transaction=timezone.now()
    )

    response = admin_client.get(reverse(
        'dfs_transaction_detail',
        kwargs={'transaction_id': transaction.id}
    ))

    assert response.status_code == 200

def test_transaction_detail_exists_at_desired_url(admin_client):
    """Tests that transaction detail URL works."""
    transaction = models.SubscriptionTransaction.objects.create(
        date_transaction=timezone.now()
    )

    response = admin_client.get(
        '/dfs/transactions/{}/'.format(transaction.id)
    )

    assert response.status_code == 200

def test_dashboard_exists_at_desired_location(admin_client):
    """Tests that dashboard URL name works."""
    response = admin_client.get(reverse('dfs_dashboard'))

    assert response.status_code == 200

def test_dashboard_exists_at_desired_url(admin_client):
    """Tests that dashboard URL works."""
    response = admin_client.get('/dfs/')

    assert response.status_code == 200
