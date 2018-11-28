"""Models for the django-flexible-subscriptions app."""
from django import models
from django.conf import setings
from django.contrib import auth
from django.utils.translation import ugettext_lazy as _


class SubscriptionPlan(models.Model):
    """Details for a subscription plan."""
    plan_name = models.CharField(
        help_text=_('the name of the subscription plan'),
        max_length=128,
    )
    plan_description = models.CharField(
        help_text=_('a description of the subscription plan'),
        max_length=512,
    )
    group = models.ForeignKey(
        auth.models.Group,
        help_text=_('the Django auth group for this plan'),
        null=True,
        on_delete=models.SET_NULL,
    )
    public = models.BooleanField(
        default=False,
        help_text=_('whether the plan is publically available'),
    )
    grace_period = models.PositiveIntegerField(
        blank=True,
        help_text=_(
            'how many days after the subscription ends before the '
            'subscription expires'
        ),
        null=True,
    )

class PlanCost(models.Model):
    """Cost and frequency of billing for a plan."""
    RECURRENCE_UNITS = (
        ('O', _('one-time')),
        ('D', _('per day')),
        ('W', _('per week')),
        ('M', _('per month')),
        ('Y', _('per year'))
    )

    plan = models.ForeignKey(
        SubscriptionPlan,
        help_text=_('the subscription plan for this user'),
        null=True,
        on_delete=models.CASCADE,
        related_name='costs',
    )
    recurrence_period = models.PositiveIntegerField(
        help_text=_('how often the plan is billed (per recurrence unit)')
    )
    recurrence_unit = models.CharField(
        choices=RECURRENCE_UNITS,
        help_text=_('the unit of measurement for the recurrence period')
        max_length=1,
    )
    cost = models.DecimalField(
        blank=True,
        decimal_places=2,
        help_text=_('the cost per recurrence of the plan'),
        max_digits=18,
        null=True,
    )

class PlanTag(models.Model):
    """Tag for a subscription plan."""
    plan = models.ForeignKey(
        SubscriptionPlan,
        help_text=_('the subscription plan for this user'),
        null=True,
        on_delete=models.CASCADE,
        related_name='tags',
    )
    tag = models.CharField(
        help_text=_('the tag name'),
        max_length=64,
    )

class UserSubscription(models.Model):
    """Details of a user's specific subscription."""
    user = models.ForeignKey(
        auth.get_user_model(),
        help_text=_('the user this subscription applies to'),
        null=True,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    plan = models.ForeignKey(
        SubscriptionPlan,
        help_text=_('the subscription plan for this user'),
        null=True,
        on_delete=models.CASCADE,
    )
    payment_method = models.ForeignKey(
        settings.FLEXIBLE_SUBSCRIPTIONS_PAYMENT_MODEL,
        help_text=_('the payment method to use for recurrent billing'),
        null=True,
        on_delete=models.CASCADE,
    )
    date_billing_start = models.DateField(
        blank=True,
        help_text=_('the date to start billing this subscription'),
        null=True,
    )
    date_billing_end = models.DateField(
        blank=True,
        help_text=_('the date to finish billing this subscription'),
        null=True,
    )
    date_billed_last = models.DateField(
        blank=True,
        help_text=_('the last date this plan was billed'),
        null=True,
    )
    date_billed_next = models.DateField(
        blank=True,
        help_text=_('the next date billing is due'),
        null=True,
    )
    active = models.BooleanField(
        default=True,
        help_text=_('whether this subscription is active or not'),
    )
    cancelled = models.BooleanField(
        default=True,
        help_text=_('whether this subscription is cancelled or not'),
    )

class SubscriptionTransaction(models.Model):
    """Details for a subscription plan billing."""
    user = models.ForeignKey(
        auth.get_user_model(),
        help_text=_('the user that this subscription was billed for'),
        null=True,
        on_delete=models.SET_NULL,
    )
    plan = models.ForeignKey(
        SubscriptionPlan,
        help_text=_('the subscription plan that was billed'),
        null=True,
        on_delete=models.SET_NULL,
    )
    date_transaction = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        help_text=_('the datetime the transaction was billed'),
    )
    amount = models.DecimalField(
        blank=True,
        decimal_places=2,
        help_text=_('how much was billed for the user'),
        max_digits=18,
        null=True,
    )
