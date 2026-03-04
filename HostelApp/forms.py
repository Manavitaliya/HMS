from django import forms
from .models import Hostel, User, Warden, Monitor


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