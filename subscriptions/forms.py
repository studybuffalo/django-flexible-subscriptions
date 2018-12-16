"""Forms for Django Flexible Subscriptions."""
# pylint: disable=invalid-name
from django import forms
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

class PaymentForm(forms.Form):
    """Form to collect details required for payment billing."""
    cardholder_name = forms.CharField(
        label='Cardholder name',
        max_length=255,
    )
    card_number = forms.CharField(
        label='Card number',
        max_length=16,
    )
    card_expiry_month = forms.CharField(
        label='Card expiry (month)',
        max_length=2,
    )
    card_expiry_year = forms.CharField(
        label='Card expiry (year)',
        max_length=4
    )
    card_cvv = forms.CharField(
        label='Card CVV',
        max_length=4,
    )

class BillingAddressForm(forms.Form):
    """Form to collect billing address deetails."""
    title = forms.CharField(
        label='Title',
        max_length=32,
    )
    name = forms.CharField(
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
    )
    address_line_3 = forms.CharField(
        label='Line 3',
        max_length=256,
    )
    city = forms.CharField(
        label='City',
        max_length=128,
    )
    province = forms.CharField(
        label='Province/State',
        max_length=128,
    )
    postcode = forms.CharField(
        label='Postcode',
        max_length=16,
    )
    country = forms.CharField(
        label='Country',
        max_length=128,
    )

def convert_widgets_to_hidden(form):
    """Converts all widgets for provided form to hidden inputs."""
    for _, field in form.__dict__['declared_fields'].items():
        field.widget = forms.HiddenInput()

    return form
