"""Factories to create Subscription Plans."""
# pylint: disable=unnecessary-lambda
from datetime import datetime

import factory

from django.contrib.auth import get_user_model

from subscriptions import models


class PlanCostFactory(factory.django.DjangoModelFactory):
    """Factory to create PlanCost model instance."""
    recurrence_period = factory.Sequence(lambda n: int(n))
    recurrence_unit = models.DAY
    cost = factory.Sequence(lambda n: int(n))

    class Meta:
        model = models.PlanCost


class SubscriptionPlanFactory(factory.django.DjangoModelFactory):
    """Factory to create SubscriptionPlan and PlanCost models."""
    plan_name = factory.Sequence(lambda n: 'Plan {}'.format(n))
    plan_description = factory.Sequence(lambda n: 'Description {}'.format(n))
    grace_period = factory.sequence(lambda n: int(n))
    cost = factory.RelatedFactory(PlanCostFactory, 'plan')

    class Meta:
        model = models.SubscriptionPlan


class PlanListDetailFactory(factory.django.DjangoModelFactory):
    """Factory to create a PlanListDetail and related SubscriptionPlan."""
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


class DFS:
    """Object to manage various model instances as needed."""
    def __init__(self):
        self._plan_list = None
        self._plan_list_detail = None
        self._plan = None
        self._cost = None
        self._subscription = None
        self._user = None

    @property
    def plan_list(self):
        """Returns the plan list instance."""
        # Create a PlanList instance if needed
        if self._plan_list:
            return self._plan_list

        # Create the PlanList instance
        self._plan_list = PlanListFactory()

        # Create the Subscription Plans
        plan_1 = SubscriptionPlanFactory()
        plan_2 = SubscriptionPlanFactory()
        plan_3 = SubscriptionPlanFactory()

        # Create the PlanList Details
        detail = PlanListDetailFactory(plan_list=self._plan_list, plan=plan_1)
        PlanListDetailFactory(plan_list=self._plan_list, plan=plan_2)
        PlanListDetailFactory(plan_list=self._plan_list, plan=plan_3)

        # Update the object attributes
        self._plan_list_detail = detail
        self._plan = plan_1
        self._cost = plan_1.costs.first()

        return self._plan_list

    @property
    def plan_list_detail(self):
        """Creates a PlanListDetail instance and associated models."""
        if self._plan_list_detail:
            return self._plan_list_detail

        # Create the model references
        self._plan_list_detail = PlanListDetailFactory()
        plan = SubscriptionPlanFactory()

        # pylint: disable=attribute-defined-outside-init
        self._plan_list_detail.plan = plan
        self._plan_list_detail.save()

        # Update the object attributes
        self._plan = plan
        self._cost = plan.costs.first()

        return self._plan_list_detail

    @property
    def plan(self):
        """Creates a SubscriptionPlan instance and associated models."""
        if self._plan:
            return self._plan

        self._plan = SubscriptionPlanFactory()

        # Update the object attributes
        self._cost = self._plan.costs.first()

        return self._plan

    @property
    def cost(self):
        """Creates a Cost instance and associated models."""
        if self._cost:
            return self._cost

        # Create a plan instance to retrieve the cost from
        self._plan  # pylint: disable=pointless-statement
        self._cost = self._plan.costs.first()

        return self._cost

    @property
    def user(self):
        """Returns the user instance."""
        if not self._user:
            self._user = UserFactory()

        return self._user

    @property
    def subscription(self):
        """Returns a UserSubscription instance."""
        if self._subscription:
            return self._subscription

        # Create user if needed
        if not self._user:
            self.user  # pylint: disable=pointless-statement

        # Create PlanCost if needed
        if not self._cost:
            self.plan  # pylint: disable=pointless-statement

        self._subscription = models.UserSubscription.objects.create(
            user=self._user,
            subscription=self._cost,
            date_billing_start=datetime(2018, 1, 1, 1, 1, 1),
            date_billing_end=None,
            date_billing_last=datetime(2018, 1, 1, 1, 1, 1),
            date_billing_next=datetime(2018, 2, 1, 1, 1, 1),
            active=True,
            cancelled=False,
        )

        return self._subscription
