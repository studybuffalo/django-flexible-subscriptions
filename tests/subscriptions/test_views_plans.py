"""Tests for the django-flexible-subscriptions SubscriptionPlan views."""
import pytest

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages import get_messages
from django.urls import reverse

from subscriptions import models


def create_tag(tag_text='test'):
    """Creates and returns a PlanTag instance."""
    return models.PlanTag.objects.create(tag=tag_text)

def create_plan(plan_name='1', plan_description='2'):
    """Creates and returns SubscriptionPlan instance."""
    return models.SubscriptionPlan.objects.create(
        plan_name=plan_name, plan_description=plan_description
    )

def create_plan_cost(plan, rec_period=1, rec_unit=models.MONTH, cost='1.00'):
    """Creates and returns a PlanCost instance."""
    return models.PlanCost.objects.create(
        plan=plan,
        recurrence_period=rec_period,
        recurrence_unit=rec_unit,
        cost=cost,
    )

# PlanListView
# -----------------------------------------------------------------------------
def test_plan_list_template(admin_client):
    """Tests for proper plan_list template."""
    response = admin_client.get(reverse('dfs_plan_list'))

    assert (
        'subscriptions/plan_list.html' in [t.name for t in response.templates]
    )

@pytest.mark.django_db
def test_plan_list_403_if_not_authorized(client, django_user_model):
    """Tests for 403 error for plan list if inadequate permissions."""
    django_user_model.objects.create_user(username='user', password='password')
    client.login(username='user', password='password')

    response = client.get(reverse('dfs_plan_list'))

    assert response.status_code == 403

@pytest.mark.django_db
def test_plan_list_200_if_authorized(client, django_user_model):
    """Tests for 200 response for plan list with adequate permissions."""
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

    response = client.get(reverse('dfs_plan_list'))

    assert response.status_code == 200

@pytest.mark.django_db
def test_plan_list_retrives_all_plans(admin_client):
    """Tests that the plan list view retrieves all the plans."""
    # Create tags to retrieve
    create_plan(plan_name='3', plan_description='c')
    create_plan(plan_name='1', plan_description='a')
    create_plan(plan_name='2', plan_description='b')

    response = admin_client.get(reverse('dfs_plan_list'))

    assert len(response.context['plans']) == 3
    assert response.context['plans'][0].plan_name == '1'
    assert response.context['plans'][1].plan_name == '2'
    assert response.context['plans'][2].plan_name == '3'

# PlanCreateView
# -----------------------------------------------------------------------------
@pytest.mark.django_db
def test_plan_create_template(admin_client):
    """Tests for proper plan_create template."""
    response = admin_client.get(reverse('dfs_plan_create'))

    assert (
        'subscriptions/plan_create.html' in [t.name for t in response.templates]
    )

@pytest.mark.django_db
def test_plan_create_403_if_not_authorized(client, django_user_model):
    """Tests for 403 error for plan create if inadequate permissions."""
    django_user_model.objects.create_user(username='user', password='password')
    client.login(username='user', password='password')

    response = client.get(reverse('dfs_plan_create'))

    assert response.status_code == 403

@pytest.mark.django_db
def test_plan_create_200_if_authorized(client, django_user_model):
    """Tests for 200 response for plan create with adequate permissions."""
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

    response = client.get(reverse('dfs_plan_create'))

    assert response.status_code == 200

@pytest.mark.django_db
def test_plan_create_create_and_success(admin_client):
    """Tests that plan creation and success message works as expected."""
    plan_count = models.SubscriptionPlan.objects.all().count()

    post_data = {
        'plan_name': '1',
        'plan_description': 'a',
        'grace_period': 0,
        'costs-TOTAL_FORMS': '0',
        'costs-INITIAL_FORMS': '0',
        'costs-MIN_NUM_FORMS': '0',
        'costs-MAX_NUM_FORMS': '1000',
    }

    response = admin_client.post(
        reverse('dfs_plan_create'),
        post_data,
        follow=True,
    )

    messages = [message for message in get_messages(response.wsgi_request)]

    assert models.SubscriptionPlan.objects.all().count() == plan_count + 1
    assert messages[0].tags == 'success'
    assert messages[0].message == 'Subscription plan successfully added'

@pytest.mark.django_db
def test_plan_create_with_costs(admin_client):
    """Tests handling of POST request with plan costs."""
    plan_count = models.SubscriptionPlan.objects.all().count()
    cost_count = models.PlanCost.objects.all().count()

    post_data = {
        'plan_name': '1',
        'plan_description': 'a',
        'grace_period': 0,
        'costs-TOTAL_FORMS': '2',
        'costs-INITIAL_FORMS': '0',
        'costs-MIN_NUM_FORMS': '0',
        'costs-MAX_NUM_FORMS': '1000',
        'costs-0-recurrence_period': '1',
        'costs-0-recurrence_unit': str(models.SECOND),
        'costs-0-cost': '1',
        'costs-1-recurrence_period': '2',
        'costs-1-recurrence_unit': str(models.HOUR),
        'costs-1-cost': '2',
    }

    admin_client.post(
        reverse('dfs_plan_create'),
        post_data,
        follow=True,
    )

    assert models.SubscriptionPlan.objects.all().count() == plan_count + 1
    assert models.PlanCost.objects.all().count() == cost_count + 2
    assert models.SubscriptionPlan.objects.last() == (
        models.PlanCost.objects.last().plan
    )

@pytest.mark.django_db
def test_plan_create_with_tags(admin_client):
    """Tests handling of POST request with tags."""
    tag_1 = create_tag('1')
    tag_2 = create_tag('2')

    post_data = {
        'plan_name': '1',
        'plan_description': 'a',
        'tags': [tag_1.id, tag_2.id],
        'grace_period': 0,
        'costs-TOTAL_FORMS': '0',
        'costs-INITIAL_FORMS': '0',
        'costs-MIN_NUM_FORMS': '0',
        'costs-MAX_NUM_FORMS': '1000',
    }

    admin_client.post(
        reverse('dfs_plan_create'),
        post_data,
        follow=True,
    )

    assert tag_1.plans.all().count() == 1
    assert tag_2.plans.all().count() == 1
    assert tag_1.plans.first() == tag_2.plans.first()

@pytest.mark.django_db
def test_plan_create_with_groups(admin_client):
    """Tests handling of POST request with groups."""
    group_1 = Group.objects.create(name='group_1')

    post_data = {
        'plan_name': '1',
        'plan_description': 'a',
        'group': group_1.id,
        'grace_period': 0,
        'costs-TOTAL_FORMS': '0',
        'costs-INITIAL_FORMS': '0',
        'costs-MIN_NUM_FORMS': '0',
        'costs-MAX_NUM_FORMS': '1000',
    }

    admin_client.post(
        reverse('dfs_plan_create'),
        post_data,
        follow=True,
    )

    assert group_1.plans.all().count() == 1
    assert models.SubscriptionPlan.objects.last() == group_1.plans.last()

@pytest.mark.django_db
def test_plan_create_invalid_form(admin_client):
    """Tests handling of invalid form submission."""
    plan_count = models.SubscriptionPlan.objects.all().count()

    post_data = {
        'plan_name': '1',
        'plan_description': 'a',
        'grace_period': 'a',
        'costs-TOTAL_FORMS': '0',
        'costs-INITIAL_FORMS': '0',
        'costs-MIN_NUM_FORMS': '0',
        'costs-MAX_NUM_FORMS': '1000',
    }

    response = admin_client.post(
        reverse('dfs_plan_create'),
        post_data,
        follow=True,
    )

    assert models.SubscriptionPlan.objects.all().count() == plan_count
    assert response.context['form'].is_valid() is False

@pytest.mark.django_db
def test_plan_create_invalid_cost_forms(admin_client):
    """Tests handling of invalid costforms submission."""
    plan_count = models.SubscriptionPlan.objects.all().count()
    cost_count = models.PlanCost.objects.all().count()

    post_data = {
        'plan_name': '1',
        'plan_description': 'a',
        'grace_period': 0,
        'costs-TOTAL_FORMS': '2',
        'costs-INITIAL_FORMS': '0',
        'costs-MIN_NUM_FORMS': '0',
        'costs-MAX_NUM_FORMS': '1000',
        'costs-0-recurrence_period': '1',
        'costs-0-recurrence_unit': 'a',
        'costs-0-cost': '1',
        'costs-1-recurrence_period': '2',
        'costs-1-recurrence_unit': 'b',
        'costs-1-cost': '2',
    }

    response = admin_client.post(
        reverse('dfs_plan_create'),
        post_data,
        follow=True,
    )

    assert models.SubscriptionPlan.objects.all().count() == plan_count
    assert models.PlanCost.objects.all().count() == cost_count
    assert response.context['form'].is_valid() is True
    assert response.context['cost_forms'].is_valid() is False

# PlanUpdateView
# -----------------------------------------------------------------------------
@pytest.mark.django_db
def test_plan_update_template(admin_client):
    """Tests for proper plan_update template."""
    plan = create_plan()

    response = admin_client.get(
        reverse('dfs_plan_update', kwargs={'plan_id': plan.id})
    )

    assert (
        'subscriptions/plan_update.html' in [t.name for t in response.templates]
    )

@pytest.mark.django_db
def test_plan_update_403_if_not_authorized(client, django_user_model):
    """Tests for 403 error for plan update if inadequate permissions."""
    plan = create_plan()

    django_user_model.objects.create_user(username='user', password='password')
    client.login(username='user', password='password')

    response = client.get(
        reverse('dfs_plan_update', kwargs={'plan_id': plan.id})
    )

    assert response.status_code == 403

@pytest.mark.django_db
def test_plan_update_200_if_authorized(client, django_user_model):
    """Tests for 200 response for plan update with adequate permissions."""
    plan = create_plan()

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
        reverse('dfs_plan_update', kwargs={'plan_id': plan.id})
    )

    assert response.status_code == 200

@pytest.mark.django_db
def test_plan_update_update_and_success(admin_client):
    """Tests that plan update and success message works as expected."""
    plan = create_plan()
    plan_count = models.SubscriptionPlan.objects.all().count()

    post_data = {
        'plan_id': plan.id,
        'plan_name': plan.plan_name,
        'plan_description': plan.plan_description,
        'grace_period': plan.grace_period,
        'costs-TOTAL_FORMS': '0',
        'costs-INITIAL_FORMS': '0',
        'costs-MIN_NUM_FORMS': '0',
        'costs-MAX_NUM_FORMS': '1000',
    }

    response = admin_client.post(
        reverse('dfs_plan_update', kwargs={'plan_id': plan.id}),
        post_data,
        follow=True,
    )

    messages = [message for message in get_messages(response.wsgi_request)]

    assert models.SubscriptionPlan.objects.all().count() == plan_count
    assert messages[0].tags == 'success'
    assert messages[0].message == 'Subscription plan successfully updated'

@pytest.mark.django_db
def test_plan_upate_with_same_costs(admin_client):
    """Tests handling of POST request with unchanged plan costs."""
    plan = create_plan()
    plan_cost = create_plan_cost(plan)

    plan_count = models.SubscriptionPlan.objects.all().count()
    cost_count = models.PlanCost.objects.all().count()

    post_data = {
        'plan_id': plan.id,
        'plan_name': plan.plan_name,
        'plan_description': plan.plan_description,
        'grace_period': plan.grace_period,
        'costs-TOTAL_FORMS': '1',
        'costs-INITIAL_FORMS': '1',
        'costs-MIN_NUM_FORMS': '0',
        'costs-MAX_NUM_FORMS': '1000',
        'costs-0-id': plan_cost.id,
        'costs-0-plan': plan_cost.plan.id,
        'costs-0-recurrence_period': plan_cost.recurrence_period,
        'costs-0-recurrence_unit': plan_cost.recurrence_unit,
        'costs-0-cost': plan_cost.cost,
        'costs-0-DELETE': False,
    }


    response = admin_client.post(
        reverse('dfs_plan_update', kwargs={'plan_id': plan.id}),
        post_data,
        follow=True,
    )

    messages = [message for message in get_messages(response.wsgi_request)]

    assert messages[0].message == 'Subscription plan successfully updated'
    assert models.SubscriptionPlan.objects.all().count() == plan_count
    assert models.PlanCost.objects.all().count() == cost_count

@pytest.mark.django_db
def test_plan_upate_with_additional_costs(admin_client):
    """Tests handling of POST request with additional plan costs."""
    plan = create_plan()
    plan_cost = create_plan_cost(plan)

    plan_count = models.SubscriptionPlan.objects.all().count()
    cost_count = models.PlanCost.objects.all().count()

    post_data = {
        'plan_id': plan.id,
        'plan_name': plan.plan_name,
        'plan_description': plan.plan_description,
        'grace_period': plan.grace_period,
        'costs-TOTAL_FORMS': '2',
        'costs-INITIAL_FORMS': '1',
        'costs-MIN_NUM_FORMS': '0',
        'costs-MAX_NUM_FORMS': '1000',
        'costs-0-id': plan_cost.id,
        'costs-0-plan': plan_cost.plan.id,
        'costs-0-recurrence_period': plan_cost.recurrence_period,
        'costs-0-recurrence_unit': plan_cost.recurrence_unit,
        'costs-0-cost': plan_cost.cost,
        'costs-0-DELETE': False,
        'costs-1-id': '',
        'costs-1-plan': '',
        'costs-1-recurrence_period': '2',
        'costs-1-recurrence_unit': str(models.HOUR),
        'costs-1-cost': '2.00',
        'costs-1-DELETE': False,
    }

    response = admin_client.post(
        reverse('dfs_plan_update', kwargs={'plan_id': plan.id}),
        post_data,
        follow=True,
    )

    messages = [message for message in get_messages(response.wsgi_request)]

    assert messages[0].message == 'Subscription plan successfully updated'
    assert models.SubscriptionPlan.objects.all().count() == plan_count
    assert models.PlanCost.objects.all().count() == cost_count + 1

@pytest.mark.django_db
def test_plan_upate_with_delete_costs(admin_client):
    """Tests handling of POST request with deleted plan costs."""
    plan = create_plan()
    plan_cost = create_plan_cost(plan)

    plan_count = models.SubscriptionPlan.objects.all().count()
    cost_count = models.PlanCost.objects.all().count()

    post_data = {
        'plan_id': plan.id,
        'plan_name': plan.plan_name,
        'plan_description': plan.plan_description,
        'grace_period': plan.grace_period,
        'costs-TOTAL_FORMS': '1',
        'costs-INITIAL_FORMS': '1',
        'costs-MIN_NUM_FORMS': '0',
        'costs-MAX_NUM_FORMS': '1000',
        'costs-0-id': plan_cost.id,
        'costs-0-plan': plan_cost.plan.id,
        'costs-0-recurrence_period': plan_cost.recurrence_period,
        'costs-0-recurrence_unit': plan_cost.recurrence_unit,
        'costs-0-cost': plan_cost.cost,
        'costs-0-DELETE': True,
    }


    response = admin_client.post(
        reverse('dfs_plan_update', kwargs={'plan_id': plan.id}),
        post_data,
        follow=True,
    )

    messages = [message for message in get_messages(response.wsgi_request)]

    assert messages[0].message == 'Subscription plan successfully updated'
    assert models.SubscriptionPlan.objects.all().count() == plan_count
    assert models.PlanCost.objects.all().count() == cost_count - 1

@pytest.mark.django_db
def test_plan_update_with_tags(admin_client):
    """Tests handling of plan update POST request with tags."""
    plan = create_plan()
    tag_1 = create_tag('1')
    tag_2 = create_tag('2')
    plan.tags.add(tag_1)
    plan.tags.add(tag_2)
    plan_tags_count = plan.tags.count()

    post_data = {
        'plan_id': plan.id,
        'plan_name': plan.plan_name,
        'plan_description': plan.plan_description,
        'tags': [tag_1.id],
        'grace_period': plan.grace_period,
        'costs-TOTAL_FORMS': '0',
        'costs-INITIAL_FORMS': '0',
        'costs-MIN_NUM_FORMS': '0',
        'costs-MAX_NUM_FORMS': '1000',
    }

    admin_client.post(
        reverse('dfs_plan_update', kwargs={'plan_id': plan.id}),
        post_data,
        follow=True,
    )

    assert plan.tags.count() == plan_tags_count - 1
    assert tag_1.plans.all().count() == 1
    assert tag_2.plans.all().count() == 0

@pytest.mark.django_db
def test_plan_update_with_groups(admin_client):
    """Tests handling of plan update POST request with groups."""
    plan = create_plan()
    group_1 = Group.objects.create(name='group_1')
    group_2 = Group.objects.create(name='group_2')
    plan.group = group_1
    plan.save()
    group_1_plan_count = group_1.plans.all().count()
    group_2_plan_count = group_2.plans.all().count()

    post_data = {
        'plan_name': '1',
        'plan_description': 'a',
        'group': group_2.id,
        'grace_period': 0,
        'costs-TOTAL_FORMS': '0',
        'costs-INITIAL_FORMS': '0',
        'costs-MIN_NUM_FORMS': '0',
        'costs-MAX_NUM_FORMS': '1000',
    }

    admin_client.post(
        reverse('dfs_plan_update', kwargs={'plan_id': plan.id}),
        post_data,
        follow=True,
    )

    assert group_1.plans.all().count() == group_1_plan_count - 1
    assert group_2.plans.all().count() == group_2_plan_count + 1

@pytest.mark.django_db
def test_plan_update_invalid_form(admin_client):
    """Tests handling of invalid form submission for updates."""
    plan = create_plan()
    plan_count = models.SubscriptionPlan.objects.all().count()

    post_data = {
        'plan_id': plan.id,
        'plan_name': plan.plan_name,
        'plan_description': plan.plan_description,
        'grace_period': 'a',
        'costs-TOTAL_FORMS': '0',
        'costs-INITIAL_FORMS': '0',
        'costs-MIN_NUM_FORMS': '0',
        'costs-MAX_NUM_FORMS': '1000',
    }

    response = admin_client.post(
        reverse('dfs_plan_update', kwargs={'plan_id': plan.id}),
        post_data,
        follow=True,
    )

    assert models.SubscriptionPlan.objects.all().count() == plan_count
    assert response.context['form'].is_valid() is False

@pytest.mark.django_db
def test_plan_update_invalid_cost_forms(admin_client):
    """Tests handling of invalid costforms submission during update."""
    plan = create_plan()
    plan_cost = create_plan_cost(plan)

    plan_count = models.SubscriptionPlan.objects.all().count()
    cost_count = models.PlanCost.objects.all().count()

    post_data = {
        'plan_id': plan.id,
        'plan_name': plan.plan_name,
        'plan_description': plan.plan_description,
        'grace_period': plan.grace_period,
        'costs-TOTAL_FORMS': '1',
        'costs-INITIAL_FORMS': '1',
        'costs-MIN_NUM_FORMS': '0',
        'costs-MAX_NUM_FORMS': '1000',
        'costs-0-id': plan_cost.id,
        'costs-0-plan': plan_cost.plan.id,
        'costs-0-recurrence_period': 'a',
        'costs-0-recurrence_unit': plan_cost.recurrence_unit,
        'costs-0-cost': plan_cost.cost,
        'costs-0-DELETE': False,
    }

    response = admin_client.post(
        reverse('dfs_plan_update', kwargs={'plan_id': plan.id}),
        post_data,
        follow=True,
    )

    assert models.SubscriptionPlan.objects.all().count() == plan_count
    assert models.PlanCost.objects.all().count() == cost_count
    assert response.context['form'].is_valid() is True
    assert response.context['cost_forms'].is_valid() is False

# TagDeleteView
# -----------------------------------------------------------------------------
@pytest.mark.django_db
def test_plan_delete_template(admin_client):
    """Tests for proper plan_delete template."""
    plan = create_plan()

    response = admin_client.get(
        reverse('dfs_plan_delete', kwargs={'plan_id': plan.id})
    )

    assert (
        'subscriptions/plan_delete.html' in [t.name for t in response.templates]
    )

@pytest.mark.django_db
def test_plan_delete_403_if_not_authorized(client, django_user_model):
    """Tests for 403 error for plan delete if inadequate permissions."""
    plan = create_plan()

    django_user_model.objects.create_user(username='user', password='password')
    client.login(username='user', password='password')

    response = client.get(
        reverse('dfs_plan_delete', kwargs={'plan_id': plan.id})
    )

    assert response.status_code == 403

@pytest.mark.django_db
def test_plan_delete_200_if_authorized(client, django_user_model):
    """Tests for 200 response for plan delete with adequate permissions."""
    plan = create_plan()

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
        reverse('dfs_plan_delete', kwargs={'plan_id': plan.id})
    )

    assert response.status_code == 200

@pytest.mark.django_db
def test_plan_delete_delete_and_success_message(admin_client):
    """Tests for success message on successful plan deletion."""
    plan = create_plan()
    plan_count = models.SubscriptionPlan.objects.all().count()

    response = admin_client.post(
        reverse('dfs_plan_delete', kwargs={'plan_id': plan.id}),
        follow=True,
    )

    messages = [message for message in get_messages(response.wsgi_request)]

    assert models.SubscriptionPlan.objects.all().count() == plan_count - 1
    assert messages[0].tags == 'success'
    assert messages[0].message == 'Subscription plan successfully deleted'
