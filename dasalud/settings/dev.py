from .base import *

#  Apps

SHARED_APPS += [
    'django_extensions',
]

INSTALLED_APPS = SHARED_APPS + list(set(TENANT_APPS) - set(SHARED_APPS))