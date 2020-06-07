"""Tests for the django-flexible-subscriptions PlanList views."""
import pytest

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages import get_messages
from django.urls import reverse

from subscriptions import models


def create_plan_list(title='test'):
    """Creates and returns a PlanList instance."""
    return models.PlanList.objects.create(title=title)


# PlanListListView
# -----------------------------------------------------------------------------
@pytest.mark.django_db
def test_plan_list_list_template(admin_client):
    """Tests for proper plan_list_list template."""
    response = admin_client.get(reverse('dfs_plan_list_list'))

    assert (
        'subscriptions/plan_list_list.html' in [
            t.name for t in response.templates
        ]
    )


@pytest.mark.django_db
def test_plan_list_list_403_if_not_authorized(client, django_user_model):
    """Tests for 403 error for PlanList list if inadequate permissions."""
    django_user_model.objects.create_user(username='user', password='password')
    client.login(username='user', password='password')

    response = client.get(reverse('dfs_plan_list_list'))

    assert response.status_code == 403


@pytest.mark.django_db
def test_plan_list_list_200_if_authorized(client, django_user_model):
    """Tests for 200 response for PlanList list with adequate permissions."""
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

    response = client.get(reverse('dfs_plan_list_list'))

    assert response.status_code == 200


@pytest.mark.django_db
def test_plan_list_list_retrieves_all_plan_lists(admin_client):
    """Tests that the list view retrieves all the plan lists."""
    # Create plan lists to retrieve
    create_plan_list('3')
    create_plan_list('1')
    create_plan_list('2')

    response = admin_client.get(reverse('dfs_plan_list_list'))

    assert len(response.context['plan_lists']) == 3
    assert response.context['plan_lists'][0].title == '3'
    assert response.context['plan_lists'][1].title == '1'
    assert response.context['plan_lists'][2].title == '2'


# PlanListCreateView
# -----------------------------------------------------------------------------
@pytest.mark.django_db
def test_plan_list_create_template(admin_client):
    """Tests for proper plan_list_create template."""
    response = admin_client.get(reverse('dfs_plan_list_create'))

    assert (
        'subscriptions/plan_list_create.html' in [
            t.name for t in response.templates
        ]
    )


@pytest.mark.django_db
def test_plan_list_create_403_if_not_authorized(client, django_user_model):
    """Tests for 403 error for PlanListCreate if inadequate permissions."""
    django_user_model.objects.create_user(username='user', password='password')
    client.login(username='user', password='password')

    response = client.get(reverse('dfs_plan_list_create'))

    assert response.status_code == 403


@pytest.mark.django_db
def test_plan_list_create_200_if_authorized(client, django_user_model):
    """Tests for 200 response for PlanListCreate with adequate permissions."""
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

    response = client.get(reverse('dfs_plan_list_create'))

    assert response.status_code == 200


@pytest.mark.django_db
def test_plan_list_create_create_and_success(admin_client):
    """Tests that plan list creation and success message works as expected."""
    plan_list_count = models.PlanList.objects.all().count()

    response = admin_client.post(
        reverse('dfs_plan_list_create'),
        {'title': '1'},
        follow=True,
    )

    messages = [message for message in get_messages(response.wsgi_request)]

    assert models.PlanList.objects.all().count() == plan_list_count + 1
    assert messages[0].tags == 'success'
    assert messages[0].message == 'Plan list successfully added'


# PlanListUpdateView
# -----------------------------------------------------------------------------
@pytest.mark.django_db
def test_plan_list_update_template(admin_client):
    """Tests for proper plan_list_update template."""
    plan_list = create_plan_list()

    response = admin_client.get(reverse(
        'dfs_plan_list_update', kwargs={'plan_list_id': plan_list.id}
    ))

    assert (
        'subscriptions/plan_list_update.html' in [
            t.name for t in response.templates
        ]
    )


@pytest.mark.django_db
def test_plan_list_update_403_if_not_authorized(client, django_user_model):
    """Tests for 403 error for PlanListUpdate if inadequate permissions."""
    plan_list = create_plan_list()

    django_user_model.objects.create_user(username='user', password='password')
    client.login(username='user', password='password')

    response = client.get(reverse(
        'dfs_plan_list_update', kwargs={'plan_list_id': plan_list.id}
    ))

    assert response.status_code == 403


@pytest.mark.django_db
def test_plan_list_update_200_if_authorized(client, django_user_model):
    """Tests for 200 response for PlanListUpdate with adequate permissions."""
    plan_list = create_plan_list()

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
        'dfs_plan_list_update', kwargs={'plan_list_id': plan_list.id}
    ))

    assert response.status_code == 200


@pytest.mark.django_db
def test_plan_list_update_update_and_success(admin_client):
    """Tests that plan list update and success message works as expected."""
    # Setup initial plan list for update
    plan_list = create_plan_list('1')
    plan_list_count = models.PlanList.objects.all().count()

    response = admin_client.post(
        reverse('dfs_plan_list_update', kwargs={'plan_list_id': plan_list.id}),
        {'title': '2'},
        follow=True,
    )

    messages = [message for message in get_messages(response.wsgi_request)]

    assert models.PlanList.objects.all().count() == plan_list_count
    assert models.PlanList.objects.get(id=plan_list.id).title == '2'
    assert messages[0].tags == 'success'
    assert messages[0].message == 'Plan list successfully updated'


# PlanListDeleteView
# -----------------------------------------------------------------------------
@pytest.mark.django_db
def test_plan_list_delete_template(admin_client):
    """Tests for proper pan_list_delete template."""
    plan_list = create_plan_list()

    response = admin_client.get(reverse(
        'dfs_plan_list_delete', kwargs={'plan_list_id': plan_list.id},
    ))

    assert (
        'subscriptions/plan_list_delete.html' in [
            t.name for t in response.templates
        ]
    )


@pytest.mark.django_db
def test_plan_list_delete_403_if_not_authorized(client, django_user_model):
    """Tests for 403 error for PlanListDelete if inadequate permissions."""
    plan_list = create_plan_list()

    django_user_model.objects.create_user(username='user', password='password')
    client.login(username='user', password='password')

    response = client.get(reverse(
        'dfs_plan_list_delete', kwargs={'plan_list_id': plan_list.id},
    ))

    assert response.status_code == 403


@pytest.mark.django_db
def test_plan_list_delete_200_if_authorized(client, django_user_model):
    """Tests for 200 response for PlanListDelete with adequate permissions."""
    plan_list = create_plan_list()

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
        'dfs_plan_list_delete', kwargs={'plan_list_id': plan_list.id},
    ))

    assert response.status_code == 200


@pytest.mark.django_db
def test_plan_list_delete_delete_and_success_message(admin_client):
    """Tests for success message on successful deletion."""
    plan_list = create_plan_list()
    plan_list_count = models.PlanList.objects.all().count()

    response = admin_client.post(
        reverse('dfs_plan_list_delete', kwargs={'plan_list_id': plan_list.id}),
        follow=True,
    )

    messages = [message for message in get_messages(response.wsgi_request)]

    assert models.PlanList.objects.all().count() == plan_list_count - 1
    assert messages[0].tags == 'success'
    assert messages[0].message == 'Plan list successfully deleted'
