from django.db import models


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1  # Always set the primary key to 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Country(models.Model):
    name = models.CharField(max_length=100)
    ultra_code = models.CharField(max_length=10, unique=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "countries"

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="states"
    )
    ultra_code = models.CharField(max_length=10, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name}, {self.country.name}"


class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="cities")
    ultra_code = models.CharField(max_length=10, unique=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "cities"

    def __str__(self):
        return f"{self.name}, {self.state.name}, {self.state.country.name}"


class GeneralConfiguration(SingletonModel):
    send_new_users_discount_email = models.BooleanField(default=True)
    new_users_discount_percentage = models.PositiveIntegerField(
        default=10, blank=True, null=True
    )
    new_users_fixed_discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, blank=True, null=True
    )

    def __str__(self):
        return "General Configuration"
