"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zm5pdbtj#33to175j^@!z37d+l2r+%00%3og764jne5#%&fm16'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

EL_PAGINATION_PER_PAGE=1
AUTHENTICATION_BACKENDS = [
    
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
    
]
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    'django.contrib.staticfiles',

    'django.contrib.sites',
    'mptt',
    'imagefit',
    "debug_toolbar",
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'ckeditor',
    "columns",
    "base",
    "accounts",
    "products"

]
IMAGEFIT_ROOT = "media"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

ACCOUNT_FORMS = {'signup': 'accounts.forms.MyCustomSignupForm'}

SOCIALACCOUNT_FORMS = {'signup': 'accounts.forms.MyCustomSocialSignupForm'}

SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
SOCIALACCOUNT_AUTO_SIGNUP=False
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL="/"
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'crum.CurrentRequestUserMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    
]

ROOT_URLCONF = 'app.urls'
AUTH_USER_MODEL = 'accounts.CustomCliente'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app.context_processors.marcas',
                'app.context_processors.category',
                'django.template.context_processors.request', ## For EL-pagination


            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "carrito",
        "HOST": "localhost",
        "USER": "postgres",
        "PASSWORD": "123",
        "port":5432
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
       
    }
}
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

LOGOUT_REDIRECT_URL="/"

MEDIA_URL = "/media/"
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  
MAILER_EMAIL_BACKEND = EMAIL_BACKEND  
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_HOST_PASSWORD = 'Sonyw395'  
EMAIL_HOST_USER = 'huacreenciso97@gmail.com'  
EMAIL_PORT = 465  
EMAIL_USE_SSL = True  
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
ACCOUNT_UNIQUE_EMAIL=True
LOGIN_REDIRECT_URL="/"

ACCOUNT_SIGNUP_REDIRECT_URL="/"
EL_PAGINATION_PER_PAGE=2   