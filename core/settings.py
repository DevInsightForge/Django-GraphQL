"""
Django settings for core project.

"""

from django.core.management.utils import get_random_secret_key

from decouple import config
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR.joinpath("templates")
STATIC_DIR = BASE_DIR.joinpath("static")
MEDIA_DIR = BASE_DIR.joinpath("media")


# Environment configurations
SECRET_KEY = config("SECRET_KEY", default=get_random_secret_key())
ON_PRODUCTION = config("ON_PRODUCTION", default=False, cast=bool)


# Database configurations
DB_ENGINE = config("DB_ENGINE", default="mysql")
DB_NAME = config("DB_NAME", default="dbname")
DB_USER = config("DB_USER", default="user")
DB_PASSWORD = config("DB_PASSWORD", default="password")
DB_HOST = config("DB_HOST", default="localhost")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=True, cast=bool)


ALLOWED_HOSTS = ["*"]


# Django built-in apps
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]


# Third Party apps
THIRD_PARTY_APPS = [
    "corsheaders",
    "django_cleanup",
    "graphene_django",
]


# local django apps
LOCAL_APPS = [
    "account",
]


# Django built-in middleware
DJANGO_MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# Third Party middleware
THIRD_PARTY_MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
]


# Application definition
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# Middleware Definition
MIDDLEWARE = DJANGO_MIDDLEWARE + THIRD_PARTY_MIDDLEWARE


# Module definition
ROOT_URLCONF = "core.urls"
ASGI_APPLICATION = "core.asgi.application"
WSGI_APPLICATION = "core.wsgi.application"
if ON_PRODUCTION:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    USE_X_FORWARDED_HOST = True


# Template Definition
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR],
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


# Database Definitions
PRODUCTION_DATABASE = {
    "ENGINE": f"django.db.backends.{DB_ENGINE}",
    "NAME": DB_NAME,
    "USER": DB_USER,
    "PASSWORD": DB_PASSWORD,
    "HOST": DB_HOST,
}

LOCAL_DATABASE = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": BASE_DIR / "db.sqlite3",
}

DATABASES = {"default": PRODUCTION_DATABASE if ON_PRODUCTION else LOCAL_DATABASE}


# Authentication Definition
AUTH_USER_MODEL = "account.User"
AUTHENTICATION_BACKENDS = [
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
]
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
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# CORS Definitions
# CORS_ALLOWED_ORIGINS = []
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True
SECURE_CROSS_ORIGIN_OPENER_POLICY = None


# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = MEDIA_DIR


# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
if ON_PRODUCTION:
    STATIC_ROOT = STATIC_DIR
else:
    STATICFILES_DIRS = [STATIC_DIR]


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Graphene definitions
GRAPHENE = {
    "SCHEMA": "core.schema.RootSchema",
    "MIDDLEWARE": [
        "graphql_jwt.middleware.JSONWebTokenMiddleware",
    ],
}


# GRAPHQL_JWT definition
GRAPHQL_JWT = {
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_EXPIRATION_DELTA": timedelta(hours=1),
    # "JWT_REFRESH_EXPIRATION_DELTA": timedelta(days=7),
    # "JWT_HIDE_TOKEN_FIELDS": True,
    # "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
    # "JWT_REUSE_REFRESH_TOKENS": True,
    # "JWT_COOKIE_SECURE": bool(ON_PRODUCTION),
    # "JWT_COOKIE_SECURE": True,
    # "JWT_COOKIE_SAMESITE": "None",
    # "JWT_COOKIE_NAME": "__a_t",
    # "JWT_REFRESH_TOKEN_COOKIE_NAME": "__r_t",
}
