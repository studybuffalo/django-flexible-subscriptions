"""Admin views for the Flexible Subscriptions app."""
from django.contrib import admin

from subscriptions import models
from django.conf import settings


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

class SubscriptionPlanInlineAdmin(admin.TabularInline):
    """Admin inline class for the SubscriptionPlan model."""
    model = models.PlanList.plans.through

class PlanListAdmin(admin.ModelAdmin):
    """Admin class for the PlanList model."""
    fields = [
        'title',
        'subtitle',
        'active'
    ]
    list_display = [
        'title',
        'subtitle',
        'header',
        'footer',
        'active'
    ]

    inlines = (SubscriptionPlanInlineAdmin,)

class UserSubscriptionAdmin(admin.ModelAdmin):
    """Admin class for the UserSubscription model."""
    fields = [
        'user',
        'date_billing_start',
        'date_billing_end',
        'date_billing_last',
        'date_billing_next',
        'active',
        'cancelled',
    ]
    list_display = [
        'user',
        'date_billing_last',
        'date_billing_next',
        'active',
        'cancelled',
    ]

class TransactionAdmin(admin.ModelAdmin):
    """Admin class for the SubscriptionTransaction model."""

if settings.DSF_ENABLE_ADMIN:
    admin.site.register(models.SubscriptionPlan, SubscriptionPlanAdmin)
    admin.site.register(models.PlanList, PlanListAdmin)
    admin.site.register(models.UserSubscription, UserSubscriptionAdmin)
    admin.site.register(models.SubscriptionTransaction, TransactionAdmin)
