import os
from pathlib import Path

# ─── BASE ──────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "insecure-secret-key")
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# ─── APPS ──────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites", 

    # Allauth core
    "allauth",
    "allauth.account",
    "allauth.socialaccount",

    # Third-party
    "rest_framework",
    "rest_framework.authtoken",
    #"corsheaders",
    "drf_yasg",  # Swagger
    "channels",
    "django_celery_beat",
    "django_celery_results",
    "django_filters",

    # Custom Apps (core)
    "apps.users",
    "apps.appointments",
    "apps.mentors",
    "apps.categories",
    "apps.courses",
    "apps.enrollments",
    "apps.gigs",
    "apps.bids",
    "apps.wallets",
    'apps.dashboard',
    'apps.learning_requests',
    "apps.transactions",
    "apps.match",
    "apps.chat",
    "apps.consultations",
    "apps.notifications",
    "apps.badges",
    "apps.support",
    "apps.mentorship_reviews",

    # Apps with custom label (fix for duplicate label issue)
    "apps.sessions.apps.CustomSessionsConfig",
    "apps.reviews.apps.ReviewsConfig",
    "apps.payments.apps.PaymentsConfig",
]

# ─── MIDDLEWARE ────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",  # Required by dj-rest-auth and allauth
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ─── URLS & ENTRY POINTS ───────────────────────────────────────────────────────
ROOT_URLCONF = "onego.urls"
WSGI_APPLICATION = "onego.wsgi.application"
ASGI_APPLICATION = "onego.asgi.application"

# ─── DATABASE ──────────────────────────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "onego_db",
        "USER": "onego_admin",
        "PASSWORD": "SAM@1234",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# ─── AUTH & I18N ───────────────────────────────────────────────────────────────
AUTH_USER_MODEL = "users.User"
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ─── STATIC & MEDIA ───────────────────────────────────────────────────────────
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "media"

# ─── CORS ──────────────────────────────────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = True
CSRF_TRUSTED_ORIGINS = ["http://localhost:3000"]


# ─── REST FRAMEWORK ────────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

# ─── CHANNELS / REDIS ──────────────────────────────────────────────────────────
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [os.getenv("REDIS_URL", "redis://localhost:6379")]},
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'apps.users.serializers.RegisterSerializer',
}
# ─── CELERY ────────────────────────────────────────────────────────────────────
CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

# ─── SWAGGER / REDOC ───────────────────────────────────────────────────────────
SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": True,
    "SECURITY_DEFINITIONS": {
        "Token": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
}
SITE_ID = 1

# ─── DJANGO-ALLAUTH SETTINGS ───────────────────────────────────────────────────
ACCOUNT_LOGIN_METHODS = {"username"}
#ACCOUNT_AUTHENTICATION_METHOD = "username"  # Replace 'ACCOUNT_LOGIN_METHODS'
ACCOUNT_SIGNUP_FIELDS = ["username", "email", "password1", "password2"]
#ACCOUNT_USERNAME_REQUIRED = True
#ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"  # Use 'mandatory' for production

# ─── EMAIL (Console for dev) ───────────────────────────────────────────────────
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ─── TEMPLATES ─────────────────────────────────────────────────────────────────
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

INSTALLED_APPS += ['corsheaders']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware'] + MIDDLEWARE

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Frontend Vite dev server
    "http://127.0.0.1:5173"
]