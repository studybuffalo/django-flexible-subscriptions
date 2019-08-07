"""Factories to create Subscription Plans."""
# pylint: disable=unnecessary-lambda
from datetime import datetime

import factory

from django.contrib.auth import get_user_model

from subscriptions import models


class PlanCostFactory(factory.django.DjangoModelFactory):
    """Factory to create PlanCost model instance."""
    recurrence_period = factory.Sequence(lambda n: int(n))
    recurrence_unit = 4
    cost = factory.Sequence(lambda n: int(n))

    class Meta:
        model = models.PlanCost

class SubscriptionPlanFactory(factory.django.DjangoModelFactory):
    """Factory to create SubscriptionPlan and PlanCost models."""
    plan_name = factory.Sequence(lambda n: 'Plan {}'.format(n))
    plan_description = factory.Sequence(lambda n: 'Description {}'.format(n))
    grace_period = factory.sequence(lambda n: int(n))

    costs1 = factory.RelatedFactory(PlanCostFactory, 'plan')
    costs2 = factory.RelatedFactory(PlanCostFactory, 'plan')

    class Meta:
        model = models.SubscriptionPlan

class PlanListDetailFactory(factory.django.DjangoModelFactory):
    """Factory to create a PlanListDetail and related SubscriptionPlan."""
    plan = factory.SubFactory(SubscriptionPlanFactory)
    html_content = factory.Sequence(lambda n: '<b>{}</b>'.format(n))
    subscribe_button_text = factory.Sequence(lambda n: 'Button {}'.format(n))
    order = factory.Sequence(lambda n: int(n))

    class Meta:
        model = models.PlanListDetail

class PlanListFactory(factory.django.DjangoModelFactory):
    """Factory to create a PlanList and all related models."""
    title = factory.Sequence(lambda n: 'Plan List {}'.format(n))
    subtitle = factory.Sequence(lambda n: 'Subtitle {}'.format(n))
    header = factory.Sequence(lambda n: 'Header {}'.format(n))
    footer = factory.Sequence(lambda n: 'Footer {}'.format(n))
    active = True

    plan_list_details1 = factory.RelatedFactory(
        PlanListDetailFactory, 'plan_list'
    )
    plan_list_details2 = factory.RelatedFactory(
        PlanListDetailFactory, 'plan_list'
    )

    class Meta:
        model = models.PlanList

class UserFactory(factory.django.DjangoModelFactory):
    """Creates a user model instance."""
    username = factory.Sequence(lambda n: 'User {}'.format(n))
    email = factory.Sequence(lambda n: 'user_{}@email.com'.format(n))
    password = 'password'

    class Meta:
        model = get_user_model()

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override _create to use the create_user method."""
        manager = cls._get_manager(model_class)

        return manager.create_user(*args, **kwargs)

def create_subscription(user, cost):
    """Creates a usser subscription."""
    return models.UserSubscription.objects.create(
        user=user,
        subscription=cost,
        date_billing_start=datetime(2018, 1, 1, 1, 1, 1),
        date_billing_end=None,
        date_billing_last=datetime(2018, 1, 1, 1, 1, 1),
        date_billing_next=datetime(2018, 2, 1, 1, 1, 1),
        active=True,
        cancelled=False,
    )
