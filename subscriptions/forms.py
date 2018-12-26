"""Forms for Django Flexible Subscriptions."""
# pylint: disable=invalid-name
from django import forms
from django.forms import ModelForm, Select

from subscriptions.conf import CURRENCY, SETTINGS
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

class PaymentForm(forms.Form):
    """Form to collect details required for payment billing."""
    cardholder_name = forms.CharField(
        label='Cardholder name',
        max_length=255,
        min_length=1,
    )
    card_number = forms.CharField(
        label='Card number',
        max_length=16,
        min_length=16,
    )
    card_expiry_month = forms.CharField(
        label='Card expiry (month)',
        max_length=2,
        min_length=1,
    )
    card_expiry_year = forms.CharField(
        label='Card expiry (year)',
        max_length=4,
        min_length=2
    )
    card_cvv = forms.CharField(
        label='Card CVV',
        max_length=4,
        min_length=3,
    )
    address_title = forms.CharField(
        label='Title',
        max_length=32,
        required=False,
    )
    address_name = forms.CharField(
        label='Name',
        max_length=128,
    )
    address_line_1 = forms.CharField(
        label='Line 1',
        max_length=256,
    )
    address_line_2 = forms.CharField(
        label='Line 2',
        max_length=256,
        required=False,
    )
    address_line_3 = forms.CharField(
        label='Line 3',
        max_length=256,
        required=False,
    )
    address_city = forms.CharField(
        label='City',
        max_length=128,
        min_length=1,
    )
    address_province = forms.CharField(
        label='Province/State',
        max_length=128,
        min_length=1,
    )
    address_postcode = forms.CharField(
        label='Postcode',
        max_length=16,
        required=False,
    )
    address_country = forms.CharField(
        label='Country',
        max_length=128,
        min_length=1,
    )

class SubscriptionPlanCostForm(forms.Form):
    """Form to handle choosing a subscription plan for payment."""
    plan_cost = forms.UUIDField(
        label='Choose subscription',
        widget=forms.RadioSelect()
    )

    def __init__(self, *args, **kwargs):
        """Overrides the plan_cost widget with available selections.

            For a provided subscription plan, provides a widget that
            lists all possible plan costs for selection.

            Keyword Arguments:
                subscription_plan (obj): A SubscriptionPlan instance.
        """
        costs = kwargs.pop('subscription_plan').costs.all()
        PLAN_COST_CHOICES = []

        for cost in costs:
            radio_text = '{} {}'.format(
                CURRENCY[SETTINGS['currency_locale']].format_currency(
                    cost.cost
                ),
                cost.display_billing_frequency_text
            )
            PLAN_COST_CHOICES.append((cost.id, radio_text))

        super(SubscriptionPlanCostForm, self).__init__(*args, **kwargs)

        # Update the radio widget with proper choices
        self.fields['plan_cost'].widget.choices = PLAN_COST_CHOICES
