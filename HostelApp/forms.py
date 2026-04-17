from django import forms
from .models import *
from django.contrib.auth.password_validation import validate_password
from datetime import date


# --------------- STUDENT ROLE -----------------

# >>>>>> STUDENT REGISTRATION FORM <<<<<<

class StudentRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

# ---------------- HOSTEL FORM ----------------

class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = ['name', 'total_rooms', 'monthly_fee']


# ---------------- USER CREATION FORM ----------------

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


# ---------------- WARDEN FORM ----------------

class WardenForm(forms.ModelForm):
    class Meta:
        model = Warden
        fields = ['user', 'hostel']


# ---------------- MONITOR FORM ----------------

class MonitorForm(forms.ModelForm):
    class Meta:
        model = Monitor
        fields = ['user']


# ---------------- APPLICATION FORM ----------------

class StudentApplicationForm(forms.ModelForm):
    class Meta:
        model = StudentApplication
        fields = ['preferred_hostel']