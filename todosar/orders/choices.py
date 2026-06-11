from django.db import models


class DiscountType(models.TextChoices):
    FIXED = "fixed"
    PERCENTAGE = "percentage"


class Status(models.TextChoices):
    CREADO = "creado"
    PAGADO = "pagado"
    ENVIADO = "enviado"
    FINALIZADO = "finalizado"
