"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


import mimetypes
mimetypes.add_type("text/css", ".css", True)
mimetypes.add_type("text/html", ".html", True)
mimetypes.add_type("text/javascript", ".js", True)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-_xspard68%xh7lalfu=sn6s@c07#l!#0en7mwn6ztn$q-(soys"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
MEDIA_URL = "/videos/"
MEDIA_ROOT = os.path.join(BASE_DIR, "videos")


# Application definition

INSTALLED_APPS = [
    "user.apps.UserConfig",
    "video.apps.VideoConfig",
    "questions.apps.QuestionsConfig",
    "descriptions.apps.DescriptionsConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "drf_yasg2",
    "rest_framework_simplejwt",
    "djoser",
    "rest_framework",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://*",
]

CORS_ALLOW_HEADERS = (
    "content-disposition",
    "access-control-allow-headers",
    "content-type",
)

#ALLOWED_HOSTS = ["https://vidscribe.org"]

CSRF_TRUSTED_ORIGINS = [ "http://localhost:3000", "http://*", "https://vidscribe.org"]

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}


# Configure Djoser settings for user registration and authentication
DJOSER = {
    "LOGIN_FIELD": "email",  # You can use 'username' instead of 'email' if needed
    "USER_CREATE_PASSWORD_RETYPE": True,
    "SEND_ACTIVATION_EMAIL": False,  # Set this to True if you want to send activation emails
}

# Replace the previous JWT settings with SimpleJWT settings
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=7),
    "SLIDING_TOKEN_LIFETIME": timedelta(days=14),
    "SLIDING_TOKEN_REFRESH_LIFETIME_GRACE_PERIOD": timedelta(days=1),
    "SLIDING_TOKEN_REFRESH_AFTER_INACTIVITY": timedelta(days=1),
    "SLIDING_TOKEN_LIFETIME_REFRESH_ON_LOGIN": True,
    "SLIDING_TOKEN_REFRESH_ON_VERSION_CHANGE": True,
    "SLIDING_TOKEN_REFRESH_ON_PASSWORD_CHANGE": True,
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'staticfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
