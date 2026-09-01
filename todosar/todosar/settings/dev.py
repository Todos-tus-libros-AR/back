import os

from .base import *  # noqa: F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DATABASE_NAME"),
        "USER": os.getenv("DATABASE_USER"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD"),
        "HOST": os.getenv("DATABASE_HOST"),
        "PORT": os.getenv("DATABASE_PORT"),
    }
}

DEBUG = True

ALLOWED_HOSTS = [
    "dev.todostuslibrosar.com.ar",
    "api.ttlar.com.ar",
    "test.ttlar.com.ar",
    "localhost",
    "127.0.0.1",
]

CSRF_TRUSTED_ORIGINS = [
    "https://dev.todostuslibrosar.com.ar",
    "https://api.ttlar.com.ar",
    "https://test.ttlar.com.ar",
    "http://localhost:5173", 
    "http://localhost:8040",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "https://test.ttlar.com.ar",
    "https://api.ttlar.com.ar",
    "https://dev.todostuslibrosar.com.ar",
]

CSRF_COOKIE_DOMAIN = None
SESSION_COOKIE_DOMAIN = None

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
