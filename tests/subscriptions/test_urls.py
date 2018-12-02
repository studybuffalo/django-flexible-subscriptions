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
    response = admin_client.get('/tags/add/')

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
