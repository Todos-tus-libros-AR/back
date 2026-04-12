from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.models import TimeStampedModel


class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)


class UserAddress(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=20)
    door = models.CharField(max_length=25, blank=True)
    postal_code = models.CharField(max_length=20)
    city = models.ForeignKey(
        "utils.City", on_delete=models.SET_NULL, null=True, related_name="addresses"
    )
    state = models.ForeignKey(
        "utils.State", on_delete=models.SET_NULL, null=True, related_name="addresses"
    )
    country = models.ForeignKey(
        "utils.Country", on_delete=models.SET_NULL, null=True, related_name="addresses"
    )
    main = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.street}, {self.number}, {self.door}, {self.city}, {self.state}, {self.postal_code}, {self.country}"
