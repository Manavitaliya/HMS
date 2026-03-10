from django import forms
from .models import *


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
        

# ---------------- STUDENT REGISTRATION FORM ----------------

class StudentRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['fname', 'mname','lname','phone_no', 'last_std', 'curr_std', 'sch_coll']


# ---------------- APPLICATION FORM ----------------

class StudentApplicationForm(forms.ModelForm):
    class Meta:
        model = StudentApplication
        fields = ['preferred_hostel']