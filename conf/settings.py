import os
import datetime
from .utils import *
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

# find and set configuration from .env file
load_dotenv(find_dotenv())

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.getenv("DEBUG"))

# comma separeted value without any space. e.g. 123,456,789
ALLOWED_HOSTS = (os.getenv("ALLOWED_HOSTS")).split(",") or []

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "django_extensions",
    "auditlog",  # https://django-auditlog.readthedocs.io/en/latest/installation.html
    "django_filters",  # https://django-filter.readthedocs.io/en/stable/guide/install.html
]

LOCAL_APPS = [
    "apps.authentication",
    "apps.common",
    "apps.document",
    "apps.rbac",
    "apps.email",
    "apps.category",
    # admin
    "apps.admin.admin_base",
    "apps.admin.admin_rbac",
    # "apps.admin.admin_menu",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # check user authentication
    "apps.common.middleware.LoginRequiredMiddleware",
    # this will expose request object to rbac.models
    "apps.common.middleware.RequestExposerMiddleware",
    "auditlog.middleware.AuditlogMiddleware",
]

ROOT_URLCONF = "conf.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            "templates",
        ],
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

WSGI_APPLICATION = "conf.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE"),
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
        "ATOMIC_REQUESTS": True,
    }
}

AUTH_USER_MODEL = "rbac.User"

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ("apps.common.rest_utils.renderers.APIJSONRenderer",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
    "EXCEPTION_HANDLER": "apps.common.rest_utils.exceptions.exception_handler",
}

# JWT config
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(hours=9),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("JWT",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": datetime.timedelta(hours=9),
    "SLIDING_TOKEN_REFRESH_LIFETIME": datetime.timedelta(days=1),
}


# Logging
# creating a log folder in basedir if not exists
if not os.path.exists(os.path.join(BASE_DIR, "log")):
    os.mkdir(os.path.join(BASE_DIR, "log"))
# Log config
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s::(%(process)d %(thread)d)::%(module)s - %(message)s"
        },
    },
    "handlers": {
        "error": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": f"log/error-{datetime.datetime.now().date()}.log",
            "formatter": "default",
        },
        "warning": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": f"log/warning-{datetime.datetime.now().date()}.log",
            "formatter": "default",
        },
        "success": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": f"log/success-{datetime.datetime.now().date()}.log",
            "formatter": "default",
        },
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["error"],
            "level": "ERROR",
            "propagate": False,
        },
        "warning_logger": {
            "handlers": ["warning"],
            "level": "WARNING",
            "propagate": False,
        },
        "success_logger": {
            "handlers": ["success"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# https://django-auditlog.readthedocs.io/en/latest/usage.html#settings
AUDITLOG_INCLUDE_ALL_MODELS = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
# STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# EMAIL Configuration
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = int(os.getenv("EMAIL_USE_TLS"))

# File Encryption key!
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")


# place this at the end of the file for developer/local configuration
try:
    from .local import *
except ModuleNotFoundError:
    pass
