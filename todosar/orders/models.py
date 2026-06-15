from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from .utils import generate_code
from .choices import DiscountType, Status


class Order(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    book_store = models.CharField(max_length=30)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        choices=Status.choices, max_length=10, default=Status.CREATED
    )
    order_link = models.CharField(max_length=200, null=True)
    order_id = models.CharField(max_length=15, null=True, blank=True)
    order_token = models.CharField(max_length=100, null=True, blank=True)


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    ean = models.CharField(max_length=13)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]
    )


class Discount(TimeStampedModel):
    code = models.CharField(max_length=15, unique=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="discounts",
    )

    type = models.CharField(choices=DiscountType.choices, max_length=10)
    percentage = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    fixed = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1)]
    )
    expiration = models.DateTimeField(null=True, blank=True)
    max_uses = models.IntegerField(default=1, validators=[MinValueValidator(1)])
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
