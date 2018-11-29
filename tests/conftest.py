"""Configuration file for pytest."""
import django
from django.conf import settings


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
        #'ROOT_URLCONF': 'flexbile_subscriptions.urls',
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
