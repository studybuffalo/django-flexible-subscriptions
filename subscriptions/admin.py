"""Admin views for the Flexible Subscriptions app."""
from django.contrib import admin

from subscriptions import models
from subscriptions.conf import SETTINGS


class PlanCostInline(admin.TabularInline):
    """Inline admin class for the PlanCost model."""
    model = models.PlanCost
    fields = (
        'slug',
        'recurrence_period',
        'recurrence_unit',
        'cost',
    )
    extra = 0

class SubscriptionPlanAdmin(admin.ModelAdmin):
    """Admin class for the SubscriptionPlan model."""
    fields = (
        'plan_name',
        'slug',
        'plan_description',
        'group',
        'tags',
        'grace_period',
    )
    inlines = [PlanCostInline]
    list_display = (
        'plan_name',
        'group',
        'display_tags',
    )
    prepopulated_fields = {'slug': ('plan_name',)}

class UserSubscriptionAdmin(admin.ModelAdmin):
    """Admin class for the UserSubscription model."""
    fields = (
        'user',
        'date_billing_start',
        'date_billing_end',
        'date_billing_last',
        'date_billing_next',
        'active',
        'cancelled',
    )
    list_display = (
        'user',
        'date_billing_last',
        'date_billing_next',
        'active',
        'cancelled',
    )

class TransactionAdmin(admin.ModelAdmin):
    """Admin class for the SubscriptionTransaction model."""

if SETTINGS['enable_admin']:
    admin.site.register(models.SubscriptionPlan, SubscriptionPlanAdmin)
    admin.site.register(models.UserSubscription, UserSubscriptionAdmin)
    admin.site.register(models.SubscriptionTransaction, TransactionAdmin)
