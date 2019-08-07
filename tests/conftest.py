"""Configuration file for pytest."""
import django
from django.conf import settings

import pytest

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
def user():
    """Returns a user model instance."""
    from . import factories

    return factories.UserFactory()

@pytest.fixture
def dfs_details():
    """Fixture that returns all required models for testing DFS."""
    from . import factories

    plan_list = factories.PlanListFactory()
    plan_detail = plan_list.plan_list_details.first()
    plan = plan_detail.plan
    cost = plan.costs.first()
    user_instance = factories.UserFactory()
    subscription = factories.create_subscription(user_instance, cost)

    return {
        'plan_list': plan_list,
        'plan_list_detail': plan_detail,
        'plan': plan,
        'cost': cost,
        'user': user_instance,
        'subscription': subscription,
    }
