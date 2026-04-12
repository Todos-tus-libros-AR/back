from django.db import models


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
