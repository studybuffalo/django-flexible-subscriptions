"""Forms for Django Flexible Subscriptions."""
# pylint: disable=invalid-name
from django.forms import ModelForm, Select

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
        RECURRENCE_UNIT_CHOICES = (
            (0, 'one-time'),
            (1, 'second'),
            (2, 'minute'),
            (3, 'hour'),
            (4, 'day'),
            (5, 'week'),
            (6, 'month'),
            (7, 'year'),
        )

        model = PlanCost
        fields = ['recurrence_period', 'recurrence_unit', 'cost']
        widgets = {
            'recurrence_unit': Select(choices=RECURRENCE_UNIT_CHOICES),
        }
