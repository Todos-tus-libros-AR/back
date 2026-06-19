from django.db import models


class DiscountType(models.TextChoices):
    FIXED = "fixed"
    PERCENTAGE = "percentage"


class Status(models.TextChoices):
    CREATED = "created"
    PAID = "paid"
    SHIPPED = "shipped"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
