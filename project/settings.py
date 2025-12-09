import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '_*&5c@1153xw6=489*2*=&*%=4)8f^m54kb@3ca-cb(wm%b@wm'

DEBUG = True   # <-- Para producción

ALLOWED_HOSTS = [
    "davidffdjango.azurewebsites.net",
    "localhost",
    "127.0.0.1"
]

CSRF_TRUSTED_ORIGINS = [
    'https://davidffdjango.azurewebsites.net',
]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap4',
    'relecloud.apps.RelecloudConfig',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'project.wsgi.application'


# --------------------------------------------------------------------
# 🔐 BASE DE DATOS — USANDO VARIABLE DE ENTORNO DE AZURE
# --------------------------------------------------------------------

DATABASES = {
    'default': dj_database_url.config(
        #default="postgres://adminpostgre:Software.@davidpostgredjango.postgres.database.azure.com:5432/relecloud_db",
        default="postgresql://adminpostgres:***@davidpostgresdjango.postgres.database.azure.com:5432/releccloud_db"
        conn_max_age=600,
        ssl_require=True
    )
}

# Si usas Azure App Settings:
# AZURE_POSTGRES_CONNECTIONSTRING = postgres://USER:PASS@HOST:5432/DB
# Sustituye default= por:
# default=os.environ.get("AZURE_POSTGRES_CONNECTIONSTRING")


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# SMTP
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USE_TLS = True

# Credenciales (todas privadas)
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

# From
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

# ReleCloud soporte interno
SUPPORT_EMAIL = os.environ.get("SUPPORT_EMAIL", EMAIL_HOST_USER)

# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login/Logout
LOGIN_REDIRECT_URL = 'index'       # después de login te lleva a la portada
LOGOUT_REDIRECT_URL = 'index'      # después de logout te lleva a la portada