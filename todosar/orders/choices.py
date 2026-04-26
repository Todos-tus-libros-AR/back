from django.db import models


class DiscountType(models.TextChoices):
    FIXED = "fixed"
    PERCENTAGE = "percentage"
