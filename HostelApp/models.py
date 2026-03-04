from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('MONITOR', 'Monitor'),
        ('WARDEN', 'Warden'),
        ('STUDENT', 'Student'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    
# Hostel model 
    
from django.conf import settings


class Hostel(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    total_rooms = models.PositiveIntegerField()
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2)

    # One warden per hostel
    warden = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'WARDEN'}
    )

    def __str__(self):
        return self.name
    
# room model

class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=10)
    capacity = models.PositiveIntegerField()
    occupied = models.PositiveIntegerField(default=0)

    def available_beds(self):
        return self.capacity - self.occupied

    def __str__(self):
        return f"{self.hostel.name} - Room {self.room_number}"
    
# StudentApplication Model

class StudentApplication(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    # Link to user (student)
    student = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'STUDENT'}
    )

    full_name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    course = models.CharField(max_length=100)
    preferred_hostel = models.ForeignKey(
        Hostel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='applications'
    )
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    applied_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.status})"
    
#StudentProfile Model

class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hostel = models.ForeignKey(Hostel, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=15)
    course = models.CharField(max_length=100)
    address = models.TextField()
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.hostel.name if self.hostel else 'No Hostel'}"
    
# 