from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1fop@ih@55$%ehzh=^+uyqnp-%a0=v5i3)=uivaxd=gj+_yhaq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# EMAIL SETTING
EMAIL_HOST_USER = "ayenimichael92@gmail.com"
EMAIL_HOST_PASSWORD = "ijky etua wexf tnmp"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_TIMEOUT = 60 * 3
