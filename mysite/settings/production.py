from .base import *
import os

# SECURITY
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = False

ALLOWED_HOSTS = ["https://vendora.pythonanywhere.com",]
HOST_BASE_URL = ALLOWED_HOSTS[0]

CSRF_TRUSTED_ORIGINS = [ALLOWED_HOSTS[0]]


STATIC_URL = '/static/'
STATICFILES_DIRS = [
        BASE_DIR / 'static',
        ]
STATIC_ROOT = BASE_DIR / '../staticfiles'
# Point this to the preferred directory. Currentlypoints upward from the BASE_DIR
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases



DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
            }
        }

# EMAIL SETTING
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_TIMEOUT = 60 * 3
