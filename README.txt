This Django application is a sort of wiki that allows users to share components
from one page "island" to another.

Your settings.py ought to include the following:

****

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'dponisetting.urls'

LOGIN_URL = '/dponiwiki/accounts/login/'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "/path/to/dponisetting/dponiwiki"
)

INSTALLED_APPS = (
    'django.contrib.auth',
	'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.markup',
    'django.contrib.sessions',
    'django.contrib.sites',
    'tagging',
    'dponisetting.dponiwiki',
)

****

