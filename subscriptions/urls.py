"""URLs for the Flexible Subscriptions app."""
from django.conf.urls import url

from subscriptions import views

urlpatterns = [
    url(r'tags/$', views.TagListView.as_view(), name='subscriptions_tag_list'),
    url(
        r'tags/add/$',
        views.TagCreateView.as_view(),
        name='subscriptions_tag_create'
    ),
    url(
        r'tags/(?P<tag_id>[0-9]+)/$',
        views.TagUpdateView.as_view(),
        name='subscriptions_tag_update'
    ),
    url(
        r'tags/(?P<tag_id>[0-9]+)/delete/$',
        views.TagDeleteView.as_view(),
        name='subscriptions_tag_delete'
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
