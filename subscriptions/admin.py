"""Admin views for the flexible_subscriptions app."""
from django.conf import settings
from django.contrib import admin

from flexible_subscriptions import models

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
    pass

if getattr(settings.FLEXIBLE_SUBSCRIPTIONS_ENABLE_ADMIN, False):
    admin.site.register(models.SubscriptionPlan, SubscriptionPlanAdmin)
    admin.site.register(models.UserSubscription, UserSubscriptionAdmin)
    admin.site.register(models.SubscriptionTransaction, TransactionAdmin)
