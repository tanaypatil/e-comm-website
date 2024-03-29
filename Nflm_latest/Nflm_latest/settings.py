"""
Django settings for Nflm_latest project.

Generated by 'django-admin startproject' using Django 1.10a1.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os
# import django
# django.setup()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8=7!k$uems!w96(ofpd43clwo@7c$(mf9uj#$dmt#a)b!95vwq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['52.204.151.211', 'nflm.co.in', 'www.nflm.co.in']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
#Apps
    'managing_users',
    'products',
    'orders',
    'carts',
    'blog',
    'wishlists',
    'reviews_and_discussion',
    'marketing',
    'voting',
    #3rd Party Apps
    'jet',
    'storages',
    'crispy_forms',
    'import_export',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Nflm_latest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Nflm_latest.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = "/home/ubuntu/Nflm_latest/static/static_root"

DEFAULT_TAX_RATE = 0.00  # 0%
DEFAULT_GIFT_WRAP_RATE = 20  # Rs: 0/-
MIN_CART_QUANTITY = 3
DEFAULT_SHIPPING_CHARGE = 0


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
# AWS_STORAGE_BUCKET_NAME = 'nflmnew-static-files'
# AWS_ACCESS_KEY_ID = 'AKIAIR45BC2YY23IMT5Q'
# AWS_SECRET_ACCESS_KEY = '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'

# Tell django-storages that when coming up with the URL for an item in S3 storage, keep
# it simple - just use this domain plus the path. (If this isn't set, things get complicated).
# This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
# We also use it in the next setting.
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# STATICFILES_LOCATION = 'static'
# STATICFILES_STORAGE = 'nflmnew.custom_storages.StaticStorage'
# STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

# STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = "/home/ubuntu/Nflm_latest/static/media/"

# MEDIAFILES_LOCATION = 'media'
# MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
# DEFAULT_FILE_STORAGE = 'nflmnew.custom_storages.MediaStorage'

# MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static", "media")
# MEDIA_ROOT = '/Users/jmitch/Desktop/ecommerce/static/media/'

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")

STATICFILES_DIRS = (
     os.path.join(os.path.dirname(BASE_DIR), "static"),
 )

# email Settings

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'skmansoormohammad@gmail.com'
EMAIL_HOST_PASSWORD = 'noormohammad'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'accounts@wedding.com'
DEFAULT_TO_EMAIL = 'to email'


# ALl Auth Settings

ACCOUNT_SIGNUP_FORM_CLASS = 'managing_users.forms.SignupForm'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"
ACCOUNT_AUTHENTICATION_METHOD="username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_UNIQUE_EMAIL = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_REQUIRED = ACCOUNT_EMAIL_REQUIRED
SOCIALACCOUNT_EMAIL_VERIFICATION = False
LOGIN_REDIRECT_URL = '/'
