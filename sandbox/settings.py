"""Django settings file to get basic Django instance running."""
from pathlib import Path

# SETTINGS FILE
# Add all environment variables to config.env in root directory
ROOT_DIR = Path(__file__).parent.absolute()

# DEBUG SETTINGS
# Used for sandbox - DO NOT USE IN PRODUCTION
DEBUG = True
TEMPLATE_DEBUG = True
SQL_DEBUG = True

# BASE DJANGO SETTINGS
SECRET_KEY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
SITE_ID = 1
INTERNAL_IPS = ('127.0.0.1',)
ROOT_URLCONF = 'urls'
APPEND_SLASH = True

# ADMIN SETTINGS
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)
MANAGERS = ADMINS

# EMAIL SETTINGS
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# LOCALIZATION SETTINGS
USE_TZ = True
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-ca'
LANGUAGES = [
    ('en-ca', 'English')
]
USE_I18N = True
USE_L10N = True

# DJANGO APPLICATIONS
INSTALLED_APPS = [
    # Django Apps
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.staticfiles',
    # External Apps
    'debug_toolbar',
    # Local Apps
    'subscriptions',
]

# DJANGO MIDDLEWARE
MIDDLEWARE = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

# DATABASE SETTINGS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(ROOT_DIR.joinpath('db.sqlite3')),
    }
}
ATOMIC_REQUESTS = True

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

# TEMPLATE SETTINGS
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            ROOT_DIR.joinpath('templates'),
        ],
        'OPTIONS': {
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
        }
    }
]

# AUTHENTICATION SETTINGS
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# STATIC SETTINGS
STATIC_URL = '/static/'
STATIC_ROOT = ROOT_DIR.joinpath('static')

# django-flexible-subscriptions settings
# -----------------------------------------------------------------------------
DFS_CURRENCY_LOCALE = 'en_ca'
DFS_ENABLE_ADMIN = True
DFS_BASE_TEMPLATE = 'subscriptions/base.html'
