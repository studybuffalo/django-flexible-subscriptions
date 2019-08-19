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
            self.process_due(subscription)

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

        payment_transaction = self.process_payment(user=user, cost=cost)

        if payment_transaction:
            # Add user to the proper group
            try:
                plan.group.user_set.add(user)
            except AttributeError:
                # No group available to add user to
                pass

            # Update subscription details
            current = timezone.now()
            next_billing = cost.next_billing_datetime(
                subscription.date_billing_start
            )
            subscription.date_billing_last = current
            subscription.date_billing_next = next_billing
            subscription.active = True
            subscription.save()

            # Record the transaction details
            self.record_transaction(
                subscription,
                self.retrieve_transaction_date(payment_transaction)
            )

            # Send notifications
            self.notify_new(subscription)

    def process_due(self, subscription):
        """Handles processing of a due subscription.

            Parameters:
                subscription (obj): A UserSubscription instance.
        """
        user = subscription.user
        cost = subscription.subscription

        payment_transaction = self.process_payment(user=user, cost=cost)

        if payment_transaction:
            # Update subscription details
            current = timezone.now()
            next_billing = cost.next_billing_datetime(
                subscription.date_billing_next
            )
            subscription.date_billing_last = current
            subscription.date_billing_next = next_billing
            subscription.save()

            # Record the transaction details
            self.record_transaction(
                subscription,
                self.retrieve_transaction_date(payment_transaction)
            )

    def process_payment(self, *args, **kwargs): # pylint: disable=unused-argument, no-self-use
        """Processes payment and confirms if payment is accepted.

            This method needs to be overriden in a project to handle
            payment processing with the appropriate payment provider.

            Can return value that evalutes to ``True`` to indicate
            payment success and any value that evalutes to ``False`` to
            indicate payment error.
        """
        return True

    def retrieve_transaction_date(self, payment): # pylint: disable=unused-argument, no-self-use
        """Returns the transaction date from provided payment details.

            Method should be overriden to accomodate the implemented
            payment processing if a more accurate datetime is required.


            Returns
                obj: The current datetime.
        """
        return timezone.now()

    @staticmethod
    def record_transaction(subscription, transaction_date=None):
        """Records transaction details in SubscriptionTransaction.

            Parameters:
                subscription (obj): A UserSubscription object.
                transaction_date (obj): A DateTime object of when
                    payment occurred (defaults to current datetime if
                    none provided).

            Returns:
                obj: The created SubscriptionTransaction instance.
        """
        if transaction_date is None:
            transaction_date = timezone.now()

        return models.SubscriptionTransaction.objects.create(
            user=subscription.user,
            subscription=subscription.subscription,
            date_transaction=transaction_date,
            amount=subscription.subscription.cost,
        )

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
