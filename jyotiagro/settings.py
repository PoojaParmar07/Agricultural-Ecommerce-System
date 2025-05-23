"""
Django settings for jyotiagro project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-lfxh@48$9io14_x^!8bu@$-3vu)^^==xyf)$5*3vwwnza4hcy9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    #local app
    'Ecommerce',
    'admin_dashboard',
    'account',
    'membership',
    'socialmedia',
    
    'django_extensions',
    'payment',
    
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

ROOT_URLCONF = 'jyotiagro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'Ecommerce.context_processors.cart_count',
                'Ecommerce.context_processors.categories_processor',
                
            ],
        },
    },
]

WSGI_APPLICATION = 'jyotiagro.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jyotiagro',
        'USER':'root',
        # 'PASSWORD':'P0#879CJ',
        'PASSWORD':'P&P1606_2307#',
        'HOST':'localhost',
        'PORT':'3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

AUTH_USER_MODEL = 'account.CustomUser'
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'media')
LOGIN_REDIRECT_URL='/admin/dashboard'
LOGIN_URL='/account/login/'
LOGOUT_REDIRECT_URL = '/account/login/'

# Looking to send emails in production? Check out our Email API/SMTP product!

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS=True

# Looking to send emails in production? Check out our Email API/SMTP product!
EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_HOST_USER = '721fb43a29876f'
EMAIL_HOST_PASSWORD = 'c5f4adeb917d43'
EMAIL_PORT = '2525'

AUTHENTICATION_BACKENDS = [
    'account.backends.EmailBackend',  # Custom backend
    'django.contrib.auth.backends.ModelBackend',  # Keep the default for admin login
]


# # Payment keys
# STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default='')
# STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY', default='')


# Razorpay
RAZORPAY_KEY_ID=config('RAZORPAY_KEY_ID',default='')
RAZORPAY_SECRET_KEY=config('RAZORPAY_SECRET_KEY',default='')
RAZORPAY_WEBHOOK_SECRET=config('RAZORPAY_WEBHOOK_SECRET',default='')
    
    
    
    
    
    
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "razorpay_webhook.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
ALLOWED_HOSTS = ['e1bf-2409-4080-9e35-ca6d-7030-2ce4-3ea0-7d73.ngrok-free.app', 'localhost', '127.0.0.1']
