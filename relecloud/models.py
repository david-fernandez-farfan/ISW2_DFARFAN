from django.db import models
from django.db.models import Count, Avg
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ValidationError
from django.urls import reverse
from django.db import models

# ============================================================
#  DESTINATION
# ============================================================

class Destination(models.Model):
    name = models.CharField(
        unique=True,
        max_length=50,
        null=False,
        blank=False,
    )
    description = models.TextField(
        max_length=2000,
        null=False,
        blank=False
    )
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("destination_detail", args=[self.id])

    # PT4 — media de reviews
    @property
    def average_rating(self):
        reviews = self.reviews.all()  # ← Cambiado review_set → reviews
        if not reviews.exists():
            return None
        return round(sum(r.rating for r in reviews) / reviews.count(), 1)

    def __str__(self):
        return self.name


# ============================================================
#  CRUISE
# ============================================================

class Cruise(models.Model):
    name = models.CharField(
        unique=True,
        max_length=50,
        null=False,
        blank=False,
    )
    description = models.TextField(
        max_length=2000,
        null=False,
        blank=False
    )
    destinations = models.ManyToManyField(
        Destination,
        related_name='cruises'
    )

    # 🔥 PT4 — media de reviews (si aplica también a cruceros)
    @property
    def average_rating(self): 
        reviews = self.reviews.all()  # ← Cambiado review_set → reviews
        if not reviews.exists():
            return None
        return round(sum(r.rating for r in reviews) / reviews.count(), 1)

    def __str__(self):
        return self.name


# ============================================================
#  INFO REQUEST
# ============================================================

class InfoRequest(models.Model):
    name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        null=True,
        blank=True,
    )
    notes = models.TextField(
        max_length=2000,
        null=True,
        blank=True,
    )
    cruise = models.ForeignKey(
        Cruise,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def __str__(self):
        # Evita devolver None → CAUSA DEL ERROR EN EL ADMIN
        if self.name:
            return self.name
        if self.email:
            return self.email
        return f"InfoRequest #{self.id}"

# ============================================================
#  PURCHASE (COMPRA)
# ============================================================

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cruise = models.ForeignKey(Cruise, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} – {self.cruise.name}"


# ============================================================
#  REVIEW MANAGER
# ============================================================

class ReviewManager(models.Manager):
    def create_review(self, user, destination=None, cruise=None, rating=0, comment=""):
        # Verifica compra (PT3)
        if not user.has_purchased(destination, cruise):
            raise PermissionDenied("User has not purchased this item")

        review = self.model(
            user=user,
            destination=destination,
            cruise=cruise,
            rating=rating,
            comment=comment
        )
        review.full_clean()  # valida rating y destino/cruise
        review.save()
        return review


# ============================================================
#  REVIEW MODEL
# ============================================================

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(
        "Destination",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    cruise = models.ForeignKey(
        "Cruise",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="reviews" 
    )
    rating = models.IntegerField()
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = ReviewManager()

    def clean(self):
        # Validación de rating
        if not 1 <= self.rating <= 5:
            raise ValidationError("Rating must be 1–5")

        # Debe tener destino o crucero
       #if not (self.destination or self.cruise):
        #   raise ValidationError("Review must reference a destination or a cruise")

    def __str__(self):
        name = self.destination.name if self.destination else self.cruise.name
        return f"{self.user.username} → {name}"


