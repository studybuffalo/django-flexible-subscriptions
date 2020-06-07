"""URLs for the sandbox demo."""

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.views.generic import TemplateView

from subscriptions import models, urls as subscriptions_urls


admin.autodiscover()

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path(
        'login/',
        LoginView.as_view(
            template_name='admin/login.html',
            extra_context={
                'title': 'django-flexible-subscriptions',
                'site_title': 'Login',
                'site_header': 'Sandbox site login',
            }
        ),
        name='login',
    ),
    path(
        'logout/',
        LogoutView.as_view(
            extra_context={
                'title': 'django-flexible-subscriptions',
                'site_title': 'Logout',
                'site_header': 'Sandbox site logout',
            }
        ),
        name='logout',
    ),
    path('subscriptions/', include(subscriptions_urls)),
    path(
        '',
        TemplateView.as_view(
            extra_context={
                'plans': models.SubscriptionPlan.objects.all()
            },
            template_name='sandbox/index.html'
        )
    ),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
