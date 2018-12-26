"""Models for the Flexible Subscriptions app."""
from datetime import timedelta
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class PlanTag(models.Model):
    """A tag for a subscription plan."""
    tag = models.CharField(
        help_text=_('the tag name'),
        max_length=64,
        unique=True,
    )

    class Meta:
        ordering = ('tag',)

    def __str__(self):
        return self.tag

class SubscriptionPlan(models.Model):
    """Details for a subscription plan."""
    id = models.UUIDField(
        default=uuid4,
        editable=False,
        primary_key=True,
        verbose_name='ID',
    )
    plan_name = models.CharField(
        help_text=_('the name of the subscription plan'),
        max_length=128,
    )
    plan_description = models.CharField(
        help_text=_('a description of the subscription plan'),
        max_length=512,
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        help_text=_('the Django auth group for this plan'),
        null=True,
        on_delete=models.SET_NULL,
        related_name='plans',
    )
    tags = models.ManyToManyField(
        PlanTag,
        blank=True,
        help_text=_('any tags associated with this plan'),
        related_name='plans',
    )
    grace_period = models.PositiveIntegerField(
        default=0,
        help_text=_(
            'how many days after the subscription ends before the '
            'subscription expires'
        ),
    )

    class Meta:
        ordering = ('plan_name',)
        permissions = (
            ('subscriptions', 'Can interact with subscription details'),
        )

    def __str__(self):
        return self.plan_name

    def display_tags(self):
        """Displays tags as a string (truncates if more than 3)."""
        if self.tags.count() > 3:
            return '{}, ...'.format(
                ', '.join(tag.tag for tag in self.tags.all()[:3])
            )

        return ', '.join(tag.tag for tag in self.tags.all()[:3])

class PlanCost(models.Model):
    """Cost and frequency of billing for a plan."""
    id = models.UUIDField(
        default=uuid4,
        editable=False,
        primary_key=True,
        verbose_name='ID',
    )
    plan = models.ForeignKey(
        SubscriptionPlan,
        help_text=_('the subscription plan for these cost details'),
        on_delete=models.CASCADE,
        related_name='costs',
    )
    recurrence_period = models.PositiveSmallIntegerField(
        default=1,
        help_text=_('how often the plan is billed (per recurrence unit)'),
        validators=[MinValueValidator(1)],
    )
    recurrence_unit = models.PositiveIntegerField(
        default=6,
        help_text=_('the unit of measurement for the recurrence period'),
        validators=[MaxValueValidator(7)],
    )
    cost = models.DecimalField(
        blank=True,
        decimal_places=4,
        help_text=_('the cost per recurrence of the plan'),
        max_digits=19,
        null=True,
    )

    class Meta:
        ordering = ('recurrence_unit', 'recurrence_period', 'cost',)

    @property
    def display_recurrent_unit_text(self):
        """Converts recurrence_unit integer to text."""
        conversion = [
            'one-time', 'per second', 'per minute', 'per hour',
            'per day', 'per week', 'per month', 'per year',
        ]

        return conversion[self.recurrence_unit]

    @property
    def display_billing_frequency_text(self):
        """Generates human-readable billing frequency."""
        conversion = [
            'one-time',
            {'singular': 'per second', 'plural': 'seconds'},
            {'singular': 'per minute', 'plural': 'minutes'},
            {'singular': 'per hour', 'plural': 'hours'},
            {'singular': 'per day', 'plural': 'days'},
            {'singular': 'per week', 'plural': 'weeks'},
            {'singular': 'per month', 'plural': 'months'},
            {'singular': 'per year', 'plural': 'years'},
        ]

        if self.recurrence_unit == 0:
            return conversion[0]

        if self.recurrence_period == 1:
            return conversion[self.recurrence_unit]['singular']

        return 'every {} {}'.format(
            self.recurrence_period, conversion[self.recurrence_unit]['plural']
        )

    def next_billing_datetime(self, current):
        """Calculates next billing date for provided datetime.

            Parameters:
                current (datetime): The current datetime to compare
                    against.

            Returns:
                datetime: The next time billing will be due.
        """
        if self.recurrence_unit == 1:
            return current + timedelta(seconds=self.recurrence_period)

        if self.recurrence_unit == 2:
            return current + timedelta(minutes=self.recurrence_period)

        if self.recurrence_unit == 3:
            return current + timedelta(hours=self.recurrence_period)

        if self.recurrence_unit == 4:
            return current + timedelta(days=self.recurrence_period)

        if self.recurrence_unit == 5:
            return current + timedelta(weeks=self.recurrence_period)

        if self.recurrence_unit == 6:
            # Adds the average number of days per month as per:
            # http://en.wikipedia.org/wiki/Month#Julian_and_Gregorian_calendars
            # This handle any issues with months < 31 days and leap years
            return current + timedelta(
                days=30.4368 * self.recurrence_period
            )

        if self.recurrence_unit == 7:
            # Adds the average number of days per year as per:
            # http://en.wikipedia.org/wiki/Year#Calendar_year
            # This handle any issues with leap years
            return current + timedelta(
                days=365.2425 * self.recurrence_period
            )

        return None

class UserSubscription(models.Model):
    """Details of a user's specific subscription."""
    id = models.UUIDField(
        default=uuid4,
        editable=False,
        primary_key=True,
        verbose_name='ID',
    )
    user = models.ForeignKey(
        get_user_model(),
        help_text=_('the user this subscription applies to'),
        null=True,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    subscription = models.ForeignKey(
        PlanCost,
        help_text=_('the plan costs and billing frequency for this user'),
        null=True,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    date_billing_start = models.DateTimeField(
        blank=True,
        help_text=_('the date to start billing this subscription'),
        null=True,
        verbose_name='billing start date',
    )
    date_billing_end = models.DateTimeField(
        blank=True,
        help_text=_('the date to finish billing this subscription'),
        null=True,
        verbose_name='billing start end',
    )
    date_billing_last = models.DateTimeField(
        blank=True,
        help_text=_('the last date this plan was billed'),
        null=True,
        verbose_name='last billing date',
    )
    date_billing_next = models.DateTimeField(
        blank=True,
        help_text=_('the next date billing is due'),
        null=True,
        verbose_name='next start date',
    )
    active = models.BooleanField(
        default=True,
        help_text=_('whether this subscription is active or not'),
    )
    cancelled = models.BooleanField(
        default=False,
        help_text=_('whether this subscription is cancelled or not'),
    )

    class Meta:
        ordering = ('user', 'date_billing_start',)

class SubscriptionTransaction(models.Model):
    """Details for a subscription plan billing."""
    id = models.UUIDField(
        default=uuid4,
        editable=False,
        primary_key=True,
        verbose_name='ID',
    )
    user = models.ForeignKey(
        get_user_model(),
        help_text=_('the user that this subscription was billed for'),
        null=True,
        on_delete=models.SET_NULL,
        related_name='subscription_transactions'
    )
    subscription = models.ForeignKey(
        PlanCost,
        help_text=_('the plan costs that were billed'),
        null=True,
        on_delete=models.SET_NULL,
        related_name='transactions'
    )
    date_transaction = models.DateTimeField(
        auto_now_add=True,
        help_text=_('the datetime the transaction was billed'),
        verbose_name='transaction date',
    )
    amount = models.DecimalField(
        blank=True,
        decimal_places=4,
        help_text=_('how much was billed for the user'),
        max_digits=19,
        null=True,
    )

    class Meta:
        ordering = ('date_transaction', 'user',)

# Convenience references for units for plan recurrence billing
ONCE = 0
SECOND = 1
MINUTE = 2
HOUR = 3
DAY = 4
WEEK = 5
MONTH = 6
YEAR = 7
