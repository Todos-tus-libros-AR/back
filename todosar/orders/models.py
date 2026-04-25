from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.conf import settings
from django.core.exceptions import ValidationError

from .utils import generate_code


class Order(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    library = models.CharField(max_length=50)
    # el número de orden será el id de la orden, a menos que se quiera un formato específico.


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    ean = models.CharField(max_length=13)
    amount = models.IntegerField()


class Discount(TimeStampedModel):
    code = models.CharField(max_length=8, unique=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="discounts",
    )

    class DiscountType(models.TextChoices):
        FIXED = "fixed"
        PERCENTAGE = "percentage"

    type = models.CharField(choices=DiscountType.choices, max_length=10)
    percentage = models.IntegerField(null=True, blank=True)
    fixed = models.IntegerField(null=True, blank=True)
    exp = models.DateTimeField(null=True, blank=True)
    max_uses = models.IntegerField(default=1)
    current_uses = models.IntegerField(default=0)

    def clean(self):
        if self.type == "fixed" and not self.fixed:
            raise ValidationError("Completar el monto fixed")
        if self.type == "fixed" and self.percentage:
            raise ValidationError(
                "Dejar vacío percentage si el descuento elegido es fixed"
            )

        if self.type == "percentage" and not self.percentage:
            raise ValidationError("Completar la cantidad percentage")
        if self.type == "percentage" and self.fixed:
            raise ValidationError(
                "Dejar vacío fixed si el descuento elegido es percentage"
            )

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_code()
        super().save(*args, **kwargs)
