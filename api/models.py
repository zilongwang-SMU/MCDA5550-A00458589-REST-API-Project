from django.db import models
import uuid


# ------------------------
# Hotel Model
# ------------------------
class Hotel(models.Model):
    hotel_name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    total_rooms = models.IntegerField(default=10)

    def __str__(self):
        return self.hotel_name


# ------------------------
# Reservation Model
# ------------------------
class Reservation(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reservations')
    checkin = models.DateField()
    checkout = models.DateField()
    confirmation_number = models.CharField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Generate confirmation number automatically
        if not self.confirmation_number:
            self.confirmation_number = f"RES-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.confirmation_number


# ------------------------
# Guest Model
# ------------------------
class Guest(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='guests')
    guest_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.guest_name