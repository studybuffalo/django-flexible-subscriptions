"""Factories to create Subscription Plans."""
import factory

from subscriptions import models


class PlanListFactory(factory.django.DjangoModelFactory):
    """Factory to create a PlanList and all related models."""
    class Meta:
        model = models.PlanList
