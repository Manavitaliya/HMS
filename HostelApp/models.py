from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


# -------------------- USER MODEL --------------------

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
    name = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=200, null=True)
    address = models.TextField(null=True, blank=True)
    total_rooms = models.IntegerField(null=True)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2)
    available_rooms = models.IntegerField(null=True) 

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


# ---------------- ROOM MODEL ----------------

class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=20)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.hostel.name} - Room {self.room_number}"


# ---------------- BED MODEL (NEW - IMPORTANT) ----------------

class Bed(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    bed_number = models.CharField(max_length=10)
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.room} - Bed {self.bed_number}"


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

    full_name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField()
    contact = models.CharField(max_length=10, unique=True)
    course = models.CharField(max_length=100)
    college_name = models.CharField(max_length=150)
    college_year = models.CharField(max_length=10, choices=YEAR_CHOICES)

    hostel = models.ForeignKey(Hostel, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    bed = models.ForeignKey(Bed, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.full_name


# ---------------- STUDENT APPLICATION ----------------

class StudentApplication(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)

    preferred_hostel = models.ForeignKey(
        Hostel,
        on_delete=models.CASCADE,
        related_name='preferred_applications'
    )

    assigned_hostel = models.ForeignKey(
        Hostel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_students'
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.status}"


# ---------------- PAYMENT MODEL ----------------

class Payment(models.Model):
    PAYMENT_STATUS = [
        ('PENDING', 'Pending'),
        ('PARTIAL', 'Partial'),
        ('PAID', 'Paid'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='PENDING')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.month}"


# ---------------- PENALTY MODEL ----------------

class Penalty(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    reason = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - Penalty"


# ---------------- COMPLAINT MODEL ----------------

class Complaint(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('RESOLVED', 'Resolved'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - Complaint"


# ---------------- LEAVE MODEL ----------------

class Leave(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.student.full_name} - Leave"