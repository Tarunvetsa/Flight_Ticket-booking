from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager

# class CustomUserManager(BaseUserManager):
#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self.create_user(email, password, **extra_fields)


# class User(AbstractUser):
#     USER = 'user'
#     ADMIN = 'admin'
#     USER_TYPE_CHOICES = [
#         (USER, 'User'),
#         (ADMIN, 'Admin'),
#     ]
    
#     name=models.CharField(max_length=200,null=True)
#     email=models.EmailField(unique=True, null=True)
#     user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default=USER)
    
#     USERNAME_FIELD='email'
#     REQUIRED_FIELDS=[]

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