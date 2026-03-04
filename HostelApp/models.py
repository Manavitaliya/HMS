from django.contrib.auth.models import AbstractUser
from django.db import models

from django.conf import settings



# --------------------USER MODEL-------------------------------

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('MONITOR', 'Monitor'),
        ('WARDEN', 'Warden'),
        ('STUDENT', 'Student'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} - {self.role}"
    


# ---------------- HOSTEL MODEL ----------------

class Hostel(models.Model):
    name = models.CharField(max_length=100)
    total_rooms = models.IntegerField()
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


# ---------------- WARDEN MODEL ----------------

class Warden(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hostel = models.OneToOneField(Hostel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.hostel.name}"


# ---------------- MONITOR MODEL ----------------

class Monitor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username