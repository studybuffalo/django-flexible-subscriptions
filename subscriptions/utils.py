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

        # Handle subscriptions with billing due
        due_subscriptions = models.UserSubscription.objects.filter(
            Q(active=True) & Q(cancelled=False)
            & Q(date_billing_next__lte=current)
        )

        for subscription in due_subscriptions:
            self.process_payment(subscription.user, subscription.subscription)

    def process_expired(self, subscription):
        """Handles processing of expired/cancelled subscriptions.

            Parameters:
                subscription (obj): A UserSubscription instance.
        """
        # Get all user subscriptions
        user = subscription.user
        user_subscriptions = user.subscriptions.all()
        subscription_group = subscription.subscription.plan.group
        group_matches = 0

        # Check if there is another subscription for this group
        for user_subscription in user_subscriptions:
            if user_subscription.subscription.plan.group == subscription_group:
                group_matches += 1

        # If no other subscription, can remove user from group
        if group_matches < 2:
            subscription_group.user_set.remove(user)

        # Update this specific UserSubscription instance
        subscription.active = False
        subscription.cancelled = True
        subscription.save()

        self.notify_expired(subscription)

    def process_new(self, subscription):
        """Handles processing of a new subscription.

            Parameters:
                subscription (obj): A UserSubscription instance.
        """
        user = subscription.user
        cost = subscription.subscription
        plan = cost.plan

        payment_success = self.process_payment(subscription.user, cost)

        if payment_success:
            # Add user to the proper group
            try:
                plan.group.user_set.add(user)
            except AttributeError:
                # No group available to add user to
                pass

            # Update subscription details
            current = timezone.now()
            next_billing = cost.next_billing_datetime(current)
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

            Parameters:
                user (obj): User instance.
                cost (str): The amount to process for payment.

            Returns:
                bool: True if payment successful, otherwise false.
        """
        return True

    def notify_expired(self, subscription):
        """Sends notification of expired subscription.

            Parameters:
                subscription (obj): A UserSubscription instance.
        """

    def notify_new(self, subscription):
        """Sends notification of newly active subscription

            Parameters:
                subscription (obj): A UserSubscription instance.
        """

    def notify_payment_error(self, subscription):
        """Sends notification of a payment error

            Parameters:
                subscription (obj): A UserSubscription instance.
        """

    def notify_payment_success(self, subscription):
        """Sends notifiation of a payment success

            Parameters:
                subscription (obj): A UserSubscription instance.
        """
