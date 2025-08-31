from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Q
from django.conf import settings
from .models import Booking

# Create your models here.

class Listing(models.Model):
    listing_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    name = models.CharField(max_length=250, null=False)
    description = models.TextField(max_length=250, null=False)
    address = models.CharField(max_length=200, null=False)
    pricepernight = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class Review(models.Model):
    review_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="reviews", null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews", null=False)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                              null=False)
    
    class Meta:
        # This is to add the check Constraint on the rating
        constraints = [
            models.CheckConstraint(
                condition=Q(rating__gte=1, rating__lte=5),
                name = "rating__valid_number"
            )
        ]
    
    def __str__(self):
        return f"{self.review_id}"

class Booking(models.Model):
    STATUS = (
        ("Pending", "pending"),
        ("Confirmed", "confirmed"),
        ("Canceled", "canceled")
    )
    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=5, decimal_places=2)
    status =  models.CharField(max_length=9, choices=STATUS, default="pending")
    created_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"User's{self.user__username} booking is: {self.status}"

class Payment(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Failed", "Failed"),
    ]
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.id} for Booking {self.booking.id} - {self.status}"

