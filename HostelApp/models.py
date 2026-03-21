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
    
    
# -------------------- ROOM MODEL --------------------

class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=20)
    capacity = models.IntegerField()
    occupied = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.hostel.name} - Room {self.room_number}"

    
# ---------------- STUDENT PROFILE ----------------

class StudentProfile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    YEAR_CHOICES = [
        ('1st', '1st Year'),
        ('2nd', '2nd Year'),
        ('3rd', '3rd Year'),
        ('4th', '4th Year'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    contact = models.CharField(max_length=10, null=True, blank=True)
    course = models.CharField(max_length=100, null=True, blank=True)
    college_name = models.CharField(max_length=150, null=True, blank=True)
    college_year = models.CharField(max_length=10, choices=YEAR_CHOICES, null=True, blank=True)

    hostel = models.ForeignKey(Hostel, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


# ---------------- STUDENT APPLICATION ----------------

class StudentApplication(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE)
    preferred_hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)

    assigned_hostel = models.ForeignKey(
        Hostel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_students'
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.student.full_name} - {self.status}"
    
    
# ---------------------STUDENT REGESTRATION------------------------------

    
    