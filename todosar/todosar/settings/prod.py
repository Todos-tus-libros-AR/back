from .base import * # noqa: F403
import os

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
    "api.todostuslibrosar.com.ar",
    "localhost",
    "127.0.0.1",
]

CSRF_TRUSTED_ORIGINS = [
    "https://api.todostuslibrosar.com.ar",
    "https://todos.apiultragestion.com.ar", 
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "https://todos.apiultragestion.com.ar",
]

SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SECURE = True