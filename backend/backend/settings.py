# flake8:noqa
from datetime import timedelta
from os import getenv
from pathlib import Path

import dotenv
from django.core.management.utils import get_random_secret_key


dotenv.load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = getenv("SECRET_KEY", get_random_secret_key())

DEBUG = getenv("DEBUG", "False").lower() in ("true", "1")

ALLOWED_HOSTS = getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
CSRF_TRUSTED_ORIGINS = getenv("CSRF_TRUSTED_ORIGINS", "").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "djoser",
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "phonenumber_field",
    "django_filters",
    "corsheaders",
    "users.apps.UsersConfig",
    "arts.apps.ArtsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"


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


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": getenv("POSTGRES_DB", "sagaart_db"),
        "USER": getenv("POSTGRES_USER", "sagaart"),
        "PASSWORD": getenv("POSTGRES_PASSWORD", ""),
        "HOST": getenv("DB_HOST", "db"),
        "PORT": getenv("DB_PORT", 5432),
    }
}


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


LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = "users.CustomUser"


STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles/static"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=5),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

DJOSER = {
    "LOGIN_FIELD": "email",
    "HIDE_USERS": False,
    "SERIALIZERS": {
        "user": "api.v1.users.serializers.CustomUserListSerializer",
    },
    "PERMISSIONS": {
        "token_create": ["rest_framework.permissions.AllowAny"],
    },
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Sagaart API",
    # "DESCRIPTION": "Your project description",
    "VERSION": "1.0.0",
}

CORS_ALLOW_ALL_ORIGINS = True

CELERY_BROKER_URL = getenv("CELERY_BROKER", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = getenv("CELERY_BACKEND", "redis://redis:6379/0")
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
