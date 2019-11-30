"""Forms for Django Flexible Subscriptions."""
# pylint: disable=invalid-name
from django import forms
from django.core import validators
from django.forms import ModelForm
from django.utils import timezone

from subscriptions.conf import CURRENCY, SETTINGS
from subscriptions.models import SubscriptionPlan, PlanCost


def assemble_cc_years():
    """Creates a list of the next 60 years."""
    cc_years = []
    now = timezone.now()

    for year in range(now.year, now.year + 60):
        cc_years.append((year, year))

    return cc_years

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

class PaymentForm(forms.Form):
    """Form to collect details required for payment billing."""
    CC_MONTHS = (
        ('1', '01 - January'),
        ('2', '02 - February'),
        ('3', '03 - March'),
        ('4', '04 - April'),
        ('5', '05 - May'),
        ('6', '06 - June'),
        ('7', '07 - July'),
        ('8', '08 - August'),
        ('9', '09 - September'),
        ('10', '10 - October'),
        ('11', '11 - November'),
        ('12', '12 - December'),
    )
    CC_YEARS = assemble_cc_years()


    cardholder_name = forms.CharField(
        label='Cardholder name',
        max_length=255,
        min_length=1,
    )
    card_number = forms.CharField(
        label='Card number',
        max_length=19,
        min_length=13,
        validators=[validators.RegexValidator(
            r'^\d{13,19}$',
            message='Invalid credit card number',
        )]
    )
    card_expiry_month = forms.ChoiceField(
        choices=CC_MONTHS,
        label='Card expiry (month)',
    )
    card_expiry_year = forms.ChoiceField(
        choices=CC_YEARS,
        label='Card expiry (year)',
    )
    card_cvv = forms.CharField(
        label='Card CVV',
        max_length=4,
        min_length=3,
        validators=[validators.RegexValidator(
            r'^\d{3,4}$',
            message='Invalid CVV2 number',
        )]
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
        label='',
        widget=forms.RadioSelect(),
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

        # Set the last value as the default
        self.fields['plan_cost'].initial = [PLAN_COST_CHOICES[-1][0]]

    def clean_plan_cost(self):
        """Validates that UUID is valid and returns model instance."""
        try:
            data = PlanCost.objects.get(id=self.cleaned_data['plan_cost'])
        except PlanCost.DoesNotExist:
            raise forms.ValidationError('Invalid plan cost submitted.')

        return data
