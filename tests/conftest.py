"""Configuration file for pytest."""
import django
from django.conf import settings

import pytest

from . import factories


def pytest_configure():
    """Setups initial testing configuration."""
    # Setup the bare minimum Django settings
    django_settings = {
        'DATABASES': {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        'INSTALLED_APPS': {
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'subscriptions',
        },
        'MIDDLEWARE': [
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ],
        'ROOT_URLCONF': 'subscriptions.urls',
        'TEMPLATES': [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
            },
        ],
    }

    settings.configure(**django_settings)

    # Initiate Django
    django.setup()

@pytest.fixture
def plan_list():
    """Fixture that returns PlanList and all related models."""
    plan_list = factories.PlanListFactory()
    plan_detail = plan_list.plan_details.first()
    plan = plan_detail.plan
    cost = plan.costs.first()

    return {
        'plan_list': plan_list,
        'plan_detail': plan_detail,
        'plan': plan,
        'cost': cost,
    }
