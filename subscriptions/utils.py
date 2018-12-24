"""Utility/helper functions for Django Flexible Subscriptions."""
from django.db.models import Q
from django.utils import timezone

from subscriptions import models


class Manager():
    """Manager object to help manage subscriptions & billing."""

    def process_subscriptions(self):
        """Calls all required subscription processing functions."""
        current = timezone.now()

        # Handle expired subscriptions
        expired_subscriptions = models.UserSubscription.objects.filter(
            Q(active=True) & Q(cancelled=False)
            & Q(date_billing_end__lte=current)
        )

        for subscription in expired_subscriptions:
            self.process_expired(subscription)

        # Handle new subscriptions
        new_subscriptions = models.UserSubscription.objects.filter(
            Q(active=False) & Q(cancelled=False)
            & Q(date_billing_start__lte=current)
        )

        for subscription in new_subscriptions:
            self.process_new(subscription)

        # Handle new subscriptions
        due_subscriptions = models.UserSubscription.objects.filter(
            Q(active=True) & Q(cancelled=False)
            & Q(date_billing_next__lte=current)
        )

        for subscription in due_subscriptions:
            self.process_payment(subscription.user, subscription.subscription)

    def process_expired(self, subscription):
        """Handles processing of expired/cancelled subscriptions."""
        # Get all user subscriptions
        user = subscription.user
        user_subscriptions = user.subscriptions

        # Remove all user groups
        user.groups.clear()

        # Re-add all active user groups
        for user_subscription in user_subscriptions:
            user_subscription.plan.group.add(user)

        # Update this specific UserSubscription instance
        subscription.active = False
        subscription.cancelled = True
        subscription.save()

        self.notify_expired(subscription)

    def process_new(self, subscription):
        """Handles processing of a new subscription."""
        payment_success = self.process_payment(
            subscription.user, subscription.subscription
        )

        if payment_success:
            # Add user to proper group
            subscription.subscription.plan.group.add(subscription.user)

            # Update subscription details
            current = timezone.now()
            next_billing = subscription.subscription.date_billing_next(current)
            subscription.date_billing_start = current
            subscription.date_billing_last = current
            subscription.date_billing_next = next_billing
            subscription.active = True
            subscription.save()

            self.notify_new(subscription)

    def process_payment(self, user=None, cost=None): # pylint: disable=unused-argument
        """Processes payment and confirms if payment is accepted.

            This method needs to be overriden in a project to handle
            payment processing with the appropriate payment provider.

            Returns:
                bool: True if payment successful, otherwise false.
        """
        return True

    def notify_expired(self, subscription):
        """Sends notification of expired subscription."""

    def notify_new(self, subscription):
        """Sends notification of newly active subscription."""

    def notify_payment_error(self, subscription):
        """Sends notification of a payment error."""

    def notify_payment_success(self, subscription):
        """Sends notifiation of a payment success."""
