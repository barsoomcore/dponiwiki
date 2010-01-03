This Django application is a sort of wiki that allows users to share components
from one page "island" to another. Along with the required .py files there is a
urls.txt file that contains the urlconf for this app, and this README file.

The contents of url.txt should be renamed "urls.py" and placed in a directory 
above dponiwiki/, where the project's manage.py and settings.py live.

Speaking of settings.py, make sure it includes the following settings:

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
    "/Users/coreyswan/Sites/dponisetting/dponiwiki"
)

INSTALLED_APPS = (
    'django.contrib.auth',
	'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.markup',
    'django.contrib.sessions',
    'django.contrib.sites',
    'tagging',
    'notification',
    'dponisetting.dponiwiki',
)

****

