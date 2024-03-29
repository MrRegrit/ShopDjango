import os
import pathlib

import django.utils.translation
import dotenv

dotenv.load_dotenv()


def load_bool(name, default):
    env_value = os.getenv(name, str(default)).lower()
    return env_value in ("t", "true", "yes", "1", "y")


def load_integer(name, default):
    env_value = os.getenv(name, str(default))
    if env_value.isdigit():
        return int(env_value)
    return 0


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "secret_key")

DEBUG = load_bool("DJANGO_DEBUG", True)

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")

ALLOW_REVERSE = load_bool("DJANGO_ALLOW_REVERSE", False)

MAIL = os.getenv("DJANGO_MAIL", "exemple@mail.com")

MAX_AUTH_ATTEMPTS = load_integer("MAX_AUTH_ATTEMPTS", 3)

if DEBUG:
    DEFAULT_USER_IS_ACTIVE = load_bool("DEFAULT_USER_IS_ACTIVE", True)
else:
    DEFAULT_USER_IS_ACTIVE = load_bool("DEFAULT_USER_IS_ACTIVE", False)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "ckeditor",
    "django_cleanup.apps.CleanupConfig",
    "sorl.thumbnail",
    "about.apps.AboutConfig",
    "catalog.apps.CatalogConfig",
    "core.apps.CoreConfig",
    "download.apps.DownloadConfig",
    "feedback.apps.FeedbackConfig",
    "homepage.apps.HomepageConfig",
    "rating.apps.RatingConfig",
    "users.apps.UsersConfig",
    "rating_statistics.apps.RatingStatisticsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "lyceum.middleware.ReversRussionWordsMiddleware",
    "users.middleware.ChangeRequestUserMiddleware",
    "users.middleware.TimezoneMiddleware",
]

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = ["127.0.0.1"]

ROOT_URLCONF = "lyceum.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "users.context_processors.birthday_users",
            ],
        },
    },
]

WSGI_APPLICATION = "lyceum.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".NumericPasswordValidator"
        ),
    },
]

TIME_ZONE = "UTC"

USE_L10N = True

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"

STATICFILES_DIRS = [BASE_DIR / "static_dev"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

LANGUAGE_CODE = "ru"

LANGUAGES = [
    ("en", django.utils.translation.gettext_lazy("English")),
    ("ru", django.utils.translation.gettext_lazy("Russian")),
]

LOGIN_URL = "/auth/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = LOGIN_URL

LOCALE_PATHS = [BASE_DIR / "locale"]

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"

EMAIL_FILE_PATH = BASE_DIR / "send_mail"

AUTHENTICATION_BACKENDS = ["users.backends.EmailOrUsernameModelBackend"]

__all__ = []
