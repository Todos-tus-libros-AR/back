import os
from celery import Celery


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv("DJANGO_SETTINGS_MODULE", "todosar.settings.prod"),
)

app = Celery("todosar")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
