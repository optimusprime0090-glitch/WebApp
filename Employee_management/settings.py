"""
Django settings for Employee_management project.

Two environments, same file:
  - Local dev  : values come from .env file (loaded by python-dotenv)
  - Azure prod : values come from App Service Environment Variables
  os.getenv() reads from whichever source is available.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# BASE_DIR = d:\Downloads\EmployeeWebApp  (the project root)
BASE_DIR = Path(__file__).resolve().parent.parent

# load_dotenv() reads the .env file in the project root when it exists.
# On Azure App Service, .env is not deployed — environment variables are
# configured directly in the portal, so load_dotenv() does nothing there.
load_dotenv()


# ---------------------------------------------------------------------------
# SECURITY SETTINGS
# ---------------------------------------------------------------------------

# SECRET_KEY must never be hardcoded in production.
# Azure: set DJANGO_SECRET_KEY in App Service → Configuration → App Settings.
# Local: set DJANGO_SECRET_KEY in your .env file.
# The fallback value is used ONLY for local development convenience.
SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    'django-insecure-local-dev-only-change-this-in-production'
)

# DEBUG must be False in production — True exposes stack traces to visitors.
# Azure: set DJANGO_DEBUG=False in App Service Environment Variables.
# Local: not set in .env, so getenv returns None → bool('') = False... 
# We use the pattern below: only True if the env var is exactly 'True'.
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'

# ALLOWED_HOSTS: list of domains Django will respond to.
# Empty = reject all requests when DEBUG=False.
# Azure: set DJANGO_ALLOWED_HOSTS=yourapp.azurewebsites.net
# Multiple domains: comma-separated  →  "app.azurewebsites.net,www.myapp.com"
# We split on comma to support multiple domains from one env var.
_allowed = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1')
ALLOWED_HOSTS = [h.strip() for h in _allowed.split(',') if h.strip()]

# CSRF_TRUSTED_ORIGINS: required when app runs behind HTTPS proxy (Azure App Service).
# Django checks the Origin header on POST requests — must match this list.
# We build it from ALLOWED_HOSTS automatically so no extra env var needed.
CSRF_TRUSTED_ORIGINS = [
    f'https://{h}' for h in ALLOWED_HOSTS if h not in ('localhost', '127.0.0.1')
] + ['http://localhost', 'http://127.0.0.1']


# ---------------------------------------------------------------------------
# APPLICATION DEFINITION
# ---------------------------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'employees',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # WhiteNoise must be IMMEDIATELY after SecurityMiddleware.
    # It intercepts /static/ requests before they reach Django's view layer
    # and serves compressed static files directly from disk.
    # This is the official WhiteNoise placement requirement.
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Employee_management.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Employee_management.wsgi.application'


# ---------------------------------------------------------------------------
# DATABASE — Azure SQL via mssql-django + pyodbc
# ---------------------------------------------------------------------------
# All credentials come from environment variables.
# Local: .env file  |  Azure: App Service Configuration → App Settings

DATABASES = {
    "default": {
        "ENGINE": "mssql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT", "1433"),
        "OPTIONS": {
            "driver": "ODBC Driver 18 for SQL Server",
            # Encrypt=yes  : enforces TLS — required by Azure SQL
            # TrustServerCertificate=no : validates Azure's SSL certificate
            "extra_params": "Encrypt=yes;TrustServerCertificate=no;",
        },
    }
}


# ---------------------------------------------------------------------------
# PASSWORD VALIDATION
# ---------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ---------------------------------------------------------------------------
# INTERNATIONALISATION
# ---------------------------------------------------------------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ---------------------------------------------------------------------------
# STATIC FILES
# ---------------------------------------------------------------------------

# URL prefix for static files in HTML: <link href="/static/css/style.css">
STATIC_URL = '/static/'

# Where Django looks for static files during development and collectstatic.
STATICFILES_DIRS = [BASE_DIR / 'static']

# collectstatic copies everything into this single folder.
# Azure App Service (Gunicorn) serves from here via WhiteNoise.
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise storage backend:
# - Compresses static files with gzip and brotli
# - Appends content hash to filenames (e.g. style.abc123.css)
#   so browsers always load the latest version after deployment
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# ---------------------------------------------------------------------------
# DEFAULT PRIMARY KEY
# ---------------------------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
