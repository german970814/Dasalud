from .base import *

#  Apps

SHARED_APPS += [
    'django_extensions',
    'debug_toolbar',
]

INSTALLED_APPS = SHARED_APPS + list(set(TENANT_APPS) - set(SHARED_APPS))

# Middleware

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'tenant_schemas.middleware.TenantMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Debug toolbar

INTERNAL_IPS = ['127.0.0.1']

# Graphene configuration

GRAPHENE['MIDDLEWARE'] = ['graphene_django.debug.DjangoDebugMiddleware']