from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import datetime
class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    
    USER_CHOICES = [
        (USER, 'User'),
        (ADMIN, 'Admin'),
    ]
    
    user_type = models.CharField(max_length=20, choices=USER_CHOICES, default=USER)

    def __str__(self):
        return f"{self.username} - {self.user_type}"
    
class Flight(models.Model):
    flight_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    departure_date=models.DateField()
    departure_time=models.TimeField()
    seat_count=models.PositiveIntegerField(default=60)
    booked_seats=models.PositiveIntegerField(default=0)
    seats_left = models.IntegerField(default=60)

    def save(self, *args, **kwargs):
        self.seats_left = self.seat_count - self.booked_seats
        super(Flight, self).save(*args, **kwargs)

    
    def __str__(self):
        return str(self.flight_number)
        
class Booking(models.Model):
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    booking_time = models.DateTimeField(default=datetime.now)
    seat_number = models.PositiveSmallIntegerField(default=1, choices=[(i, i) for i in range(1, 61)])

    def __str__(self):
        return str(self.booking_id)