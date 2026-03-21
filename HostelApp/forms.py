from django import forms
from .models import *
from django.contrib.auth.password_validation import validate_password
from datetime import date


class StudentRegisterForm(forms.ModelForm):
    # Account Fields
    password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    # Hostel
    preferred_hostel = forms.ModelChoiceField(queryset=Hostel.objects.all())

    # Profile Fields
    full_name = forms.CharField(max_length=100)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=StudentProfile.GENDER_CHOICES)
    address = forms.CharField(widget=forms.Textarea)
    contact = forms.CharField(max_length=10)
    course = forms.CharField(max_length=100)
    college_name = forms.CharField(max_length=150)
    college_year = forms.ChoiceField(choices=StudentProfile.YEAR_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    # Password Match Validation
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    # Contact Validation
    def clean_contact(self):
        contact = self.cleaned_data.get('contact')

        if not contact.isdigit():
            raise forms.ValidationError("Contact must contain only digits")

        if len(contact) != 10:
            raise forms.ValidationError("Contact must be exactly 10 digits")

        return contact

    # Age Validation
    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        today = date.today()

        if dob > today:
            raise forms.ValidationError("DOB cannot be in the future")

        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        if age < 16:
            raise forms.ValidationError("Student must be at least 16 years old")

        return dob


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