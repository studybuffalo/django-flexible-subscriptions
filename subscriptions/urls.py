"""URLs for the Flexible Subscriptions app."""
# pylint: disable=line-too-long
from django.conf.urls import url
from django.views.generic import TemplateView

from subscriptions import views


urlpatterns = [
    url(
        r'tags/$',
        views.TagListView.as_view(),
        name='subscriptions_tag_list',
    ),
    url(
        r'tags/create/$',
        views.TagCreateView.as_view(),
        name='subscriptions_tag_create',
    ),
    url(
        r'tags/(?P<tag_id>[0-9]+)/$',
        views.TagUpdateView.as_view(),
        name='subscriptions_tag_update',
    ),
    url(
        r'tags/(?P<tag_id>[0-9]+)/delete/$',
        views.TagDeleteView.as_view(),
        name='subscriptions_tag_delete',
    ),
    url(
        r'plans/$',
        views.PlanListView.as_view(),
        name='subscriptions_plan_list',
    ),
    url(
        r'plans/create/$',
        views.PlanCreateView.as_view(),
        name='subscriptions_plan_create',
    ),
    url(
        r'plans/(?P<plan_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',
        views.PlanUpdateView.as_view(),
        name='subscriptions_plan_update',
    ),
    url(
        r'plans/(?P<plan_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/delete/$',
        views.PlanDeleteView.as_view(),
        name='subscriptions_plan_delete',
    ),
    url(
        r'subscriptions/$',
        views.SubscriptionListView.as_view(),
        name='subscriptions_subscription_list',
    ),
    url(
        r'subscriptions/create/$',
        views.SubscriptionCreateView.as_view(),
        name='subscriptions_subscription_create',
    ),
    url(
        r'subscriptions/(?P<plan_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',
        views.SubscriptionUpdateView.as_view(),
        name='subscriptions_subscription_update',
    ),
    url(
        r'subscriptions/(?P<plan_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/delete/$',
        views.SubscriptionDeleteView.as_view(),
        name='subscriptions_subscription_delete',
    ),
    url(
        r'transactions/$',
        views.TransactionListView.as_view(),
        name='subscriptions_transaction_list',
    ),
    url(
        r'transactions/(?P<transaction_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',
        views.TransactionDetailView.as_view(),
        name='subscriptions_transaction_detail',
    ),
    url(
        r'^$',
        TemplateView.as_view(template_name='subscriptions/index.html'),
        name='subscriptions_index',
    ),
]

# URL for viewing all subscriptions

# URL for viewing a specific subscription
# URL to modify specific fields of subscription
# URL to add a subscription
# Cancel subscription - set stop date?

# URL to view all subscription plans
# URL to create a subscription plan
# URL to inactivate a subscription plan (use a date here?)
# URL to modify subscription plan (e.g. tags)? or require a new one?

# URL to view payment transactions
