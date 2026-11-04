"""Minimal Django settings for standalone PDF XBlock tests."""
SECRET_KEY = 'standalone-pdf-tests-only'
INSTALLED_APPS = ()
USE_I18N = True
LANGUAGE_CODE = 'en'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'APP_DIRS': True}]
