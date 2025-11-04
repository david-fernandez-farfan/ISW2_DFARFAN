from django.db import models

# Create your models here.
class Destination(models.Model):
    name = models.CharField(
        unique=True,
        null=False,
        blank=False,
        max_length=50
    )
    description = models.TextField(
        max_length=2000,
        null=False,
        blank=False
    )

    def __str__(self):
        return self.name


class Cruise(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        blank=False
    )
    description = models.TextField(
        max_length=2000,
        null=False,
        blank=False
    )
    departure_date = models.DateField(
        null=False,
        blank=False
    )
    return_date = models.DateField(
        null=False,
        blank=False
    )
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name="cruises"
    )

    def __str__(self):
        return f"{self.name} ({self.departure_date} → {self.return_date})"


class InfoRequest(models.Model):
    full_name = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )
    email = models.EmailField(
        null=False,
        blank=False
    )
    message = models.TextField(
        max_length=2000,
        null=False,
        blank=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    cruise = models.ForeignKey(
        Cruise,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="info_requests"
    )

    def __str__(self):
        return f"Request from {self.full_name} ({self.email})"
