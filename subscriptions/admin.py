"""Admin views for the Flexible Subscriptions app."""
from django.contrib import admin

from subscriptions import models
from subscriptions.conf import SETTINGS


class SubscriptionPlanAdmin(admin.ModelAdmin):
    """Admin class for the SubscriptionPlan model."""
    fields = [
        'plan_name',
        'plan_description',
        'group',
        'tags',
        'grace_period',
    ]
    list_display = [
        'plan_name',
        'group',
        'display_tags',
    ]

class UserSubscriptionAdmin(admin.ModelAdmin):
    """Admin class for the UserSubscription model."""
    fields = [
        'user',
        'plan',
        'payment_method',
        'date_billing_start',
        'date_billing_end',
        'date_billing_last',
        'date_billing_next',
        'active',
        'cancelled',
    ]
    list_display = [
        'user',
        'plan',
        'date_billing_last',
        'date_billing_next',
        'active',
        'cancelled',
    ]

class TransactionAdmin(admin.ModelAdmin):
    """Admin class for the SubscriptionTransaction model."""

if SETTINGS['enable_admin']:
    admin.site.register(models.SubscriptionPlan, SubscriptionPlanAdmin)
    admin.site.register(models.UserSubscription, UserSubscriptionAdmin)
    admin.site.register(models.SubscriptionTransaction, TransactionAdmin)
