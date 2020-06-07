"""Tests for the DashboardView"""
import pytest

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from subscriptions import models


def test_dashboard_template(admin_client):
    """Tests for proper plan_list template."""
    response = admin_client.get(reverse('dfs_dashboard'))

    assert (
        'subscriptions/dashboard.html' in [t.name for t in response.templates]
    )


@pytest.mark.django_db
def test_dashboard_403_if_not_authorized(client, django_user_model):
    """Tests for 403 error for plan list if inadequate permissions."""
    django_user_model.objects.create_user(username='a', password='b')
    client.login(username='a', password='b')

    response = client.get(reverse('dfs_dashboard'))

    assert response.status_code == 403


@pytest.mark.django_db
def test_dashboard_200_if_authorized(client, django_user_model):
    """Tests for 200 response for plan list with adequate permissions."""
    # Retrieve proper permission, add to user, and login
    content = ContentType.objects.get_for_model(models.SubscriptionPlan)
    permission = Permission.objects.get(
        content_type=content, codename='subscriptions'
    )
    user = django_user_model.objects.create_user(username='a', password='b')
    user.user_permissions.add(permission)
    client.login(username='a', password='b')

    response = client.get(reverse('dfs_dashboard'))

    assert response.status_code == 200
