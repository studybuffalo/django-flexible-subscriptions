"""Tests for the django-flexible-subscriptions PlanListDetail views."""
import pytest

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages import get_messages
from django.urls import reverse

from subscriptions import models


pytestmark = pytest.mark.django_db  # pylint: disable=invalid-name

def create_plan_list(title='test'):
    """Creates and returns a PlanList instance."""
    return models.PlanList.objects.create(title=title)

def create_plan(plan_name='1', plan_description='2'):
    """Creates and returns SubscriptionPlan instance."""
    return models.SubscriptionPlan.objects.create(
        plan_name=plan_name, plan_description=plan_description
    )

def create_plan_list_detail(plan=None, plan_list=None):
    """Creates and returns PlanListDetail instance."""
    if not plan:
        plan = create_plan()

    if not plan_list:
        plan_list = create_plan_list()

    return models.PlanListDetail.objects.create(
        plan=plan, plan_list=plan_list
    )


# PlanListDetailListView
# -----------------------------------------------------------------------------
def test_detail_list_template(admin_client):
    """Tests for proper plan_list_detail_list template."""
    plan_list = create_plan_list()

    response = admin_client.get(reverse(
        'dfs_plan_list_detail_list', kwargs={'plan_list_id': plan_list.id}
    ))

    assert (
        'subscriptions/plan_list_detail_list.html' in [
            t.name for t in response.templates
        ]
    )

def test_detail_list_403_if_not_authorized(client, django_user_model):
    """Tests for 403 error for PlanListDetail list if inadequate permissions."""
    django_user_model.objects.create_user(username='user', password='password')
    client.login(username='user', password='password')

    plan_list = create_plan_list()

    response = client.get(reverse(
        'dfs_plan_list_detail_list', kwargs={'plan_list_id': plan_list.id}
    ))

    assert response.status_code == 403

def test_detail_list_200_if_authorized(client, django_user_model):
    """Tests for 200 response for detail list adequate permissions."""
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

    plan_list = create_plan_list()

    response = client.get(reverse(
        'dfs_plan_list_detail_list', kwargs={'plan_list_id': plan_list.id}
    ))

    assert response.status_code == 200

def test_detail_list_adds_plan_list_context(admin_client):
    """Tests that Detail list view adds plan_list to context."""
    plan_list = create_plan_list()

    response = admin_client.get(reverse(
        'dfs_plan_list_detail_list', kwargs={'plan_list_id': plan_list.id}
    ))

    assert 'plan_list' in response.context
    assert response.context['plan_list'].id == plan_list.id


# # PlanListCreateView
# -----------------------------------------------------------------------------
def test_detail_create_template(admin_client):
    """Tests for proper plan_list_detail_create template."""
    plan_list = create_plan_list()

    response = admin_client.get(reverse(
        'dfs_plan_list_detail_create', kwargs={'plan_list_id': plan_list.id}
    ))

    assert (
        'subscriptions/plan_list_detail_create.html' in [
            t.name for t in response.templates
        ]
    )

def test_detail_create_403_if_not_authorized(client, django_user_model):
    """Tests for 403 error for PlanListCreate if inadequate permissions."""
    django_user_model.objects.create_user(username='user', password='password')
    client.login(username='user', password='password')

    plan_list = create_plan_list()

    response = client.get(reverse(
        'dfs_plan_list_detail_create', kwargs={'plan_list_id': plan_list.id}
    ))

    assert response.status_code == 403

def test_detail_create_200_if_authorized(client, django_user_model):
    """Tests for 200 response for Detail create with adequate permissions."""
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

    plan_list = create_plan_list()

    response = client.get(reverse(
        'dfs_plan_list_detail_create', kwargs={'plan_list_id': plan_list.id}
    ))

    assert response.status_code == 200

def test_detail_create_create_and_success(admin_client):
    """Tests detail creation and success message."""
    plan = create_plan()
    plan_list = create_plan_list()
    detail_count = models.PlanListDetail.objects.all().count()

    response = admin_client.post(
        reverse(
            'dfs_plan_list_detail_create',
            kwargs={'plan_list_id': plan_list.id}
        ),
        {
            'plan': plan.id,
            'plan_list': plan_list.id,
            'title': '1',
        },
        follow=True,
    )

    messages = [message for message in get_messages(response.wsgi_request)]

    assert models.PlanListDetail.objects.all().count() == detail_count + 1
    assert messages[0].tags == 'success'
    assert messages[0].message == (
        'Subscription plan successfully added to plan list'
    )

def test_detail_create_adds_plan_list_context(admin_client):
    """Tests that Detail create view adds plan_list to context."""
    plan_list = create_plan_list()

    response = admin_client.get(reverse(
        'dfs_plan_list_detail_create', kwargs={'plan_list_id': plan_list.id}
    ))

    assert 'plan_list' in response.context
    assert response.context['plan_list'].id == plan_list.id

def test_detail_create_creates_proper_url(admin_client):
    """Tests that Detail create view generates proper success URL."""
    plan = create_plan()
    plan_list = create_plan_list()

    response = admin_client.post(
        reverse(
            'dfs_plan_list_detail_create',
            kwargs={'plan_list_id': plan_list.id}
        ),
        {
            'plan': plan.id,
            'plan_list': plan_list.id,
            'title': '1',
        },
        follow=True,
    )
    success_url, _ = response.redirect_chain[-1]

    assert success_url == '/dfs/plan-lists/{}/details/'.format(plan_list.id)

# # PlanListUpdateView
# -----------------------------------------------------------------------------
def test_detail_update_template(admin_client):
    """Tests for proper plan_list_detail_update template."""
    plan_list = create_plan_list()
    detail = create_plan_list_detail(plan_list=plan_list)

    response = admin_client.get(reverse(
        'dfs_plan_list_detail_update',
        kwargs={'plan_list_id': plan_list.id, 'plan_list_detail_id': detail.id}
    ))

    assert (
        'subscriptions/plan_list_detail_update.html' in [
            t.name for t in response.templates
        ]
    )

def test_detail_update_403_if_not_authorized(client, django_user_model):
    """Tests for 403 error for Detail update if inadequate permissions."""
    plan_list = create_plan_list()
    detail = create_plan_list_detail(plan_list=plan_list)

    django_user_model.objects.create_user(username='user', password='password')
    client.login(username='user', password='password')

    response = client.get(reverse(
        'dfs_plan_list_detail_update',
        kwargs={'plan_list_id': plan_list.id, 'plan_list_detail_id': detail.id}
    ))

    assert response.status_code == 403

def test_detail_update_200_if_authorized(client, django_user_model):
    """Tests for 200 response for Detail Update with adequate permissions."""
    plan_list = create_plan_list()
    detail = create_plan_list_detail(plan_list=plan_list)

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
        'dfs_plan_list_detail_update',
        kwargs={'plan_list_id': plan_list.id, 'plan_list_detail_id': detail.id}
    ))

    assert response.status_code == 200

def test_detail_update_update_and_success(admin_client):
    """Tests that plan list update and success message works as expected."""
    plan = create_plan()
    plan_list = create_plan_list()
    detail = models.PlanListDetail.objects.create(
        plan=plan, plan_list=plan_list
    )
    detail_count = models.PlanListDetail.objects.all().count()

    response = admin_client.post(
        reverse(
            'dfs_plan_list_detail_update',
            kwargs={
                'plan_list_id': plan_list.id,
                'plan_list_detail_id': detail.id,
            }
        ),
        {
            'plan': plan.id,
            'plan_list': plan_list.id,
            'html_content': '<b>Test</b>',
        },
        follow=True,
    )

    messages = [message for message in get_messages(response.wsgi_request)]

    assert models.PlanListDetail.objects.all().count() == detail_count
    assert models.PlanListDetail.objects.get(id=plan_list.id).html_content == (
        '<b>Test</b>'
    )
    assert messages[0].tags == 'success'
    assert messages[0].message == 'Plan list details successfully updated'

def test_detail_update_adds_plan_list_context(admin_client):
    """Tests that Detail update view adds plan_list to context."""
    plan_list = create_plan_list()
    detail = create_plan_list_detail(plan_list=plan_list)

    response = admin_client.get(reverse(
        'dfs_plan_list_detail_update',
        kwargs={'plan_list_id': plan_list.id, 'plan_list_detail_id': detail.id}
    ))

    assert 'plan_list' in response.context
    assert response.context['plan_list'].id == plan_list.id

def test_detail_update_creates_proper_url(admin_client):
    """Tests that Detail update view generates proper success URL."""
    plan = create_plan()
    plan_list = create_plan_list()
    detail = create_plan_list_detail(plan=plan, plan_list=plan_list)

    response = admin_client.post(
        reverse(
            'dfs_plan_list_detail_update',
            kwargs={
                'plan_list_id': plan_list.id,
                'plan_list_detail_id': detail.id,
            }
        ),
        {
            'plan': plan.id,
            'plan_list': plan_list.id,
        },
        follow=True,
    )
    success_url, _ = response.redirect_chain[-1]

    assert success_url == '/dfs/plan-lists/{}/details/'.format(plan_list.id)

# PlanListDeleteView
# -----------------------------------------------------------------------------
def test_detail_delete_template(admin_client):
    """Tests for proper plan_list_detail_delete template."""
    plan_list = create_plan_list()
    detail = create_plan_list_detail(plan_list=plan_list)

    response = admin_client.get(reverse(
        'dfs_plan_list_detail_delete',
        kwargs={'plan_list_id': plan_list.id, 'plan_list_detail_id': detail.id}
    ))

    assert (
        'subscriptions/plan_list_detail_delete.html' in [
            t.name for t in response.templates
        ]
    )

def test_detail_delete_403_if_not_authorized(client, django_user_model):
    """Tests for 403 error for Detail delete if inadequate permissions."""
    plan_list = create_plan_list()
    detail = create_plan_list_detail(plan_list=plan_list)

    django_user_model.objects.create_user(username='user', password='password')
    client.login(username='user', password='password')

    response = client.get(reverse(
        'dfs_plan_list_detail_delete',
        kwargs={'plan_list_id': plan_list.id, 'plan_list_detail_id': detail.id}
    ))

    assert response.status_code == 403

def test_detail_delete_200_if_authorized(client, django_user_model):
    """Tests for 200 response for Detail delete with adequate permissions."""
    plan_list = create_plan_list()
    detail = create_plan_list_detail(plan_list=plan_list)

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
        'dfs_plan_list_detail_delete',
        kwargs={'plan_list_id': plan_list.id, 'plan_list_detail_id': detail.id}
    ))

    assert response.status_code == 200

def test_detail_delete_delete_and_success_message(admin_client):
    """Tests for success message on successful deletion."""
    plan_list = create_plan_list()
    detail = create_plan_list_detail(plan_list=plan_list)
    detail_count = models.PlanListDetail.objects.all().count()

    response = admin_client.post(
        reverse(
            'dfs_plan_list_detail_delete',
            kwargs={
                'plan_list_id': plan_list.id,
                'plan_list_detail_id': detail.id
            }
        ),
        follow=True,
    )

    messages = [message for message in get_messages(response.wsgi_request)]

    assert models.PlanListDetail.objects.all().count() == detail_count - 1
    assert messages[0].tags == 'success'
    assert messages[0].message == (
        'Subscription plan successfully removed from plan list'
    )

def test_detail_delete_creates_proper_url(admin_client):
    """Tests that Detail delete view generates proper success URL."""
    plan = create_plan()
    plan_list = create_plan_list()
    detail = create_plan_list_detail(plan=plan, plan_list=plan_list)

    response = admin_client.post(
        reverse(
            'dfs_plan_list_detail_delete',
            kwargs={
                'plan_list_id': plan_list.id,
                'plan_list_detail_id': detail.id,
            }
        ),
        follow=True,
    )
    success_url, _ = response.redirect_chain[-1]

    assert success_url == '/dfs/plan-lists/{}/details/'.format(plan_list.id)
