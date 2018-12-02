"""Tests for the django-flexible-subscriptions views module."""
import pytest

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages import get_messages
from django.urls import reverse

from subscriptions import models


def create_tag(tag_text='test'):
    """Creates and returns a PlanTag instance."""
    return models.PlanTag.objects.create(tag=tag_text)

# TagListView
# -----------------------------------------------------------------------------
@pytest.mark.django_db
def test_tag_list_template(admin_client):
    """Tests for proper tag_list template."""
    response = admin_client.get(reverse('subscriptions_tag_list'))

    assert (
        'subscriptions/tag_list.html' in [t.name for t in response.templates]
    )

@pytest.mark.django_db
def test_tag_list_403_if_not_authorized(client, django_user_model):
    """Tests for 403 error for tag list if inadequate permissions."""
    django_user_model.objects.create_user(username='user', password='password')
    client.login(username='user', password='password')

    response = client.get(reverse('subscriptions_tag_list'))

    assert response.status_code == 403

@pytest.mark.django_db
def test_tag_list_200_if_authorized(client, django_user_model):
    """Tests for 200 response for tag list with adequate permissions."""
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

    response = client.get(reverse('subscriptions_tag_list'))

    assert response.status_code == 200


# TagCreateView
# -----------------------------------------------------------------------------
@pytest.mark.django_db
def test_tag_create_template(admin_client):
    """Tests for proper tag_create template."""
    response = admin_client.get(reverse('subscriptions_tag_create'))

    assert (
        'subscriptions/tag_create.html' in [t.name for t in response.templates]
    )

@pytest.mark.django_db
def test_tag_create_403_if_not_authorized(client, django_user_model):
    """Tests for 403 error for tag create if inadequate permissions."""
    django_user_model.objects.create_user(username='user', password='password')
    client.login(username='user', password='password')

    response = client.get(reverse('subscriptions_tag_create'))

    assert response.status_code == 403

@pytest.mark.django_db
def test_tag_create_200_if_authorized(client, django_user_model):
    """Tests for 200 response for tag create with adequate permissions."""
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

    response = client.get(reverse('subscriptions_tag_create'))

    assert response.status_code == 200


# TagUpdateView
# -----------------------------------------------------------------------------
@pytest.mark.django_db
def test_tag_update_template(admin_client):
    """Tests for proper tag_update template."""
    tag = create_tag()

    response = admin_client.get(reverse(
        'subscriptions_tag_update', kwargs={'tag_id': tag.id}
    ))

    assert (
        'subscriptions/tag_update.html' in [t.name for t in response.templates]
    )

@pytest.mark.django_db
def test_tag_update_403_if_not_authorized(client, django_user_model):
    """Tests for 403 error for tag update if inadequate permissions."""
    tag = create_tag()

    django_user_model.objects.create_user(username='user', password='password')
    client.login(username='user', password='password')

    response = client.get(reverse(
        'subscriptions_tag_update', kwargs={'tag_id': tag.id}
    ))

    assert response.status_code == 403

@pytest.mark.django_db
def test_tag_update_200_if_authorized(client, django_user_model):
    """Tests for 200 response for tag update with adequate permissions."""
    tag = create_tag()

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

    response = client.get(reverse(
        'subscriptions_tag_update', kwargs={'tag_id': tag.id}
    ))

    assert response.status_code == 200


# TagDeleteView
# -----------------------------------------------------------------------------
@pytest.mark.django_db
def test_tag_delete_template(admin_client):
    """Tests for proper tag_delete template."""
    tag = create_tag()

    response = admin_client.get(reverse(
        'subscriptions_tag_delete', kwargs={'tag_id': tag.id},
    ))

    assert (
        'subscriptions/tag_delete.html' in [t.name for t in response.templates]
    )

@pytest.mark.django_db
def test_tag_delete_403_if_not_authorized(client, django_user_model):
    """Tests for 403 error for tag delete if inadequate permissions."""
    tag = create_tag()

    django_user_model.objects.create_user(username='user', password='password')
    client.login(username='user', password='password')

    response = client.get(reverse(
        'subscriptions_tag_delete', kwargs={'tag_id': tag.id},
    ))

    assert response.status_code == 403

@pytest.mark.django_db
def test_tag_delete_200_if_authorized(client, django_user_model):
    """Tests for 200 response for tag delete with adequate permissions."""
    tag = create_tag()

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

    response = client.get(reverse(
        'subscriptions_tag_delete', kwargs={'tag_id': tag.id},
    ))

    assert response.status_code == 200

@pytest.mark.django_db
def test_tag_delete_message_on_success(admin_client):
    """Tests for success message on successful deletion."""
    tag = create_tag()

    response = admin_client.post(
        reverse('subscriptions_tag_delete', kwargs={'tag_id': tag.id}),
        follow=True,
    )

    messages = [message for message in get_messages(response.wsgi_request)]

    assert response.status_code == 200
    assert messages[0].tags == 'success'
    assert messages[0].message == 'Tag successfully deleted'
