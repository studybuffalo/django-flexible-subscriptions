"""Forms for Django Flexible Subscriptions."""
# pylint: disable=invalid-name
from django.forms import ModelForm

from subscriptions.models import SubscriptionPlan, PlanCost


class SubscriptionPlanForm(ModelForm):
    """Model Form for SubscriptionPlan model."""
    class Meta:
        model = SubscriptionPlan
        fields = [
            'plan_name', 'plan_description', 'group', 'tags', 'grace_period',
        ]

class PlanCostForm(ModelForm):
    """Form to use with inlineformset_factory and SubscriptionPlanForm."""
    class Meta:
        model = PlanCost
        fields = ['recurrence_period', 'recurrence_unit', 'cost']
