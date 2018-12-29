"""Tests for the django-flexible-subscriptions PlanTag views."""
from decimal import Decimal
import pytest

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone

from subscriptions import models


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

def create_transaction(user, cost, amount='1.00'):
    """Creates and returns a PlanTag instance."""
    return models.SubscriptionTransaction.objects.create(
        user=user,
        subscription=cost,
        date_transaction=timezone.now(),
        amount=amount,
    )

# TransactionListView
# -----------------------------------------------------------------------------
@pytest.mark.django_db
def test_transaction_list_template(admin_client):
    """Tests for proper transaction_list template."""
    response = admin_client.get(reverse('dfs_transaction_list'))

    assert 'subscriptions/transaction_list.html' in [
        t.name for t in response.templates
    ]

@pytest.mark.django_db
def test_transaction_list_403_if_not_authorized(client, django_user_model):
    """Tests for 403 error for tag list if inadequate permissions."""
    django_user_model.objects.create_user(username='user', password='password')
    client.login(username='user', password='password')

    response = client.get(reverse('dfs_tag_list'))

    assert response.status_code == 403

@pytest.mark.django_db
def test_transaction_list_200_if_authorized(client, django_user_model):
    """Tests 200 response for transaction list with adequate permissions."""
    # Retrieve proper permission, add to user, and login
    content = ContentType.objects.get_for_model(models.SubscriptionPlan)
    permission = Permission.objects.get(
        content_type=content, codename='subscriptions'
    )
    user = django_user_model.objects.create_user(
        username='user', password='password'
    )
    user.user_permissions.add(permission)
    client.login(username='user', password='password')

    response = client.get(reverse('dfs_tag_list'))

    assert response.status_code == 200

@pytest.mark.django_db
def test_transaction_list_retrives_all(admin_client, django_user_model):
    """Tests that the list view retrieves all the transactions."""
    # Create transactions to retrieve
    user = django_user_model.objects.create_user(username='a', password='b')
    cost = create_cost(plan=create_plan())
    create_transaction(user, cost, '1.00')
    create_transaction(user, cost, '2.00')
    create_transaction(user, cost, '3.00')

    response = admin_client.get(reverse('dfs_transaction_list'))

    assert len(response.context['transactions']) == 3
    assert response.context['transactions'][0].amount == Decimal('1.0000')
    assert response.context['transactions'][1].amount == Decimal('2.0000')
    assert response.context['transactions'][2].amount == Decimal('3.0000')

# TransactionDetailView
# -----------------------------------------------------------------------------
@pytest.mark.django_db
def test_transaction_detail_template(admin_client, django_user_model):
    """Tests for proper transaction_detail template."""
    user = django_user_model.objects.create_user(username='a', password='b')
    cost = create_cost(plan=create_plan())
    transaction = create_transaction(user, cost)

    response = admin_client.get(
        reverse(
            'dfs_transaction_detail',
            kwargs={'transaction_id': transaction.id}
        )
    )

    assert 'subscriptions/transaction_detail.html' in [
        t.name for t in response.templates
    ]

@pytest.mark.django_db
def test_transaction_detail_403_if_not_authorized(client, django_user_model):
    """Tests  403 error for transaction detail if inadequate permissions."""
    user = django_user_model.objects.create_user(username='a', password='b')
    cost = create_cost(plan=create_plan())
    transaction = create_transaction(user, cost)

    django_user_model.objects.create_user(username='user', password='password')
    client.login(username='user', password='password')

    response = client.get(
        reverse(
            'dfs_transaction_detail',
            kwargs={'transaction_id': transaction.id}
        )
    )

    assert response.status_code == 403

@pytest.mark.django_db
def test_transaction_detail_200_if_authorized(client, django_user_model):
    """Tests 200 response for transaction detail with adequate permissions."""
    user = django_user_model.objects.create_user(username='a', password='b')
    cost = create_cost(plan=create_plan())
    transaction = create_transaction(user, cost)

    # Retrieve proper permission, add to user, and login
    content = ContentType.objects.get_for_model(models.SubscriptionPlan)
    permission = Permission.objects.get(
        content_type=content, codename='subscriptions'
    )
    user = django_user_model.objects.create_user(
        username='user', password='password'
    )
    user.user_permissions.add(permission)
    client.login(username='user', password='password')

    response = client.get(
        reverse(
            'dfs_transaction_detail',
            kwargs={'transaction_id': transaction.id}
        )
    )

    assert response.status_code == 200
