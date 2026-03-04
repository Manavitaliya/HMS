from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User

from .models import *
from .forms import *
from django.contrib import messages


# ---------------- LOGIN ----------------

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('redirect_dashboard')
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid Credentials'})

    return render(request, 'registration/login.html')


# ---------------- REDIRECT BASED ON ROLE ----------------

@login_required
def redirect_dashboard(request):

    if request.user.role == 'ADMIN':
        return redirect('admin_dashboard')

    elif request.user.role == 'MONITOR':
        return redirect('monitor_dashboard')

    elif request.user.role == 'WARDEN':
        return redirect('warden_dashboard')

    elif request.user.role == 'STUDENT':
        return redirect('student_dashboard')

    return redirect('login')


# ---------------- LOGOUT ----------------

def logout_view(request):
    logout(request)
    return redirect('login')


# ---------------- DASHBOARDS ----------------

@login_required
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')


@login_required
def monitor_dashboard(request):
    return render(request, 'monitor/dashboard.html')


@login_required
def warden_dashboard(request):
    return render(request, 'warden/dashboard.html')


@login_required
def student_dashboard(request):
    return render(request, 'student/dashboard.html')


# ----------------------CREATE HOSTEL--------------------------------

@login_required
def create_hostel(request):
    if request.user.role != 'ADMIN':
        return redirect('login')

    form = HostelForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Hostel Created Successfully")
        return redirect('view_hostels')

    return render(request, 'admin/create_hostel.html', {'form': form})

# ---------------------VIEW HOSTELS-------------------------

@login_required
def view_hostels(request):
    if request.user.role != 'ADMIN':
        return redirect('login')

    hostels = Hostel.objects.all()
    return render(request, 'admin/view_hostels.html', {'hostels': hostels})

# --------------------CREATE MONITOT-----------------------------

@login_required
def create_monitor(request):
    if request.user.role != 'ADMIN':
        return redirect('login')

    user_form = UserForm(request.POST or None)

    if user_form.is_valid():
        user = user_form.save(commit=False)
        user.role = 'MONITOR'
        user.set_password(user.password)
        user.save()

        Monitor.objects.create(user=user)

        messages.success(request, "Monitor Created Successfully")
        return redirect('admin_dashboard')

    return render(request, 'admin/create_monitor.html', {'form': user_form})


# --------------------CREATE WARDEN-------------------------------

@login_required
def create_warden(request):
    if request.user.role != 'ADMIN':
        return redirect('login')

    user_form = UserForm(request.POST or None)

    if user_form.is_valid():
        user = user_form.save(commit=False)
        user.role = 'WARDEN'
        user.set_password(user.password)
        user.save()

        return redirect('assign_warden', user_id=user.id)

    return render(request, 'admin/create_warden.html', {'form': user_form})




# ---------------------ASSIGN WARDEN TO HOSTEL-----------------------------

@login_required
def assign_warden(request, user_id):
    if request.user.role != 'ADMIN':
        return redirect('login')

    user = User.objects.get(id=user_id)

    # Only show hostels that don't have a warden yet
    available_hostels = Hostel.objects.filter(warden__isnull=True)

    form = WardenForm(request.POST or None)
    form.fields['hostel'].queryset = available_hostels

    if request.method == 'POST':
        if form.is_valid():
            warden = form.save(commit=False)
            warden.user = user
            warden.save()
            messages.success(request, "Warden Assigned Successfully")
            return redirect('view_wardens')

    return render(request, 'admin/assign_warden.html', {'form': form})


# -------------------- VIEW MONITOR-----------------------------------

@login_required
def view_monitors(request):
    if request.user.role != 'ADMIN':
        return redirect('login')

    monitors = Monitor.objects.all()
    return render(request, 'admin/view_monitors.html', {'monitors': monitors})


# ----------------------VIEW WARDENS---------------------------------


@login_required
def view_wardens(request):
    if request.user.role != 'ADMIN':
        return redirect('login')

    wardens = Warden.objects.select_related('user', 'hostel')
    return render(request, 'admin/view_wardens.html', {'wardens': wardens})


# ----------------------DELETE FUNCTIONS------------------------------------

@login_required # FOR MONITOR
def delete_monitor(request, id):
    if request.user.role != 'ADMIN':
        return redirect('login')

    monitor = Monitor.objects.get(id=id)
    monitor.user.delete()
    monitor.delete()

    return redirect('view_monitors')


@login_required # FOR WARDEN
def delete_warden(request, id):
    if request.user.role != 'ADMIN':
        return redirect('login')

    warden = Warden.objects.get(id=id)
    warden.user.delete()
    warden.delete()

    return redirect('view_wardens')


# -----------------STUDENT DASHBOARD-----------------------------------


@login_required
def student_dashboard(request):
    if request.user.role != 'STUDENT':
        return redirect('login')

    return render(request, 'student/dashboard.html')

# ---------------- STUDENT REGISTER ----------------

def student_register(request):
    form = StudentRegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        user.role = 'STUDENT'
        user.set_password(user.password)
        user.save()

        StudentProfile.objects.create(user=user)

        messages.success(request, "Registration Successful. Please Login.")
        return redirect('login')

    return render(request, 'student/register.html', {'form': form})


# ---------------- VIEW HOSTELS (STUDENT) ----------------

@login_required
def student_view_hostels(request):
    if request.user.role != 'STUDENT':
        return redirect('login')

    hostels = Hostel.objects.all()
    return render(request, 'student/view_hostels.html', {'hostels': hostels})


# ---------------- APPLY FOR HOSTEL ----------------

@login_required
def apply_hostel(request):
    if request.user.role != 'STUDENT':
        return redirect('login')

    if StudentApplication.objects.filter(student=request.user).exists():
        messages.error(request, "You already applied.")
        return redirect('student_dashboard')

    form = StudentApplicationForm(request.POST or None)

    if form.is_valid():
        application = form.save(commit=False)
        application.student = request.user
        application.save()
        messages.success(request, "Application Submitted Successfully")
        return redirect('student_dashboard')

    return render(request, 'student/apply_hostel.html', {'form': form})


# ----------------------MONITOR DASHBOARD------------------------------------

@login_required
def monitor_dashboard(request):
    if request.user.role != 'MONITOR':
        return redirect('login')

    return render(request, 'monitor/dashboard.html')


# ---------------------VIEW APPLICATION (MONITIR)--------------------------

@login_required
def view_applications(request):
    if request.user.role != 'MONITOR':
        return redirect('login')

    applications = StudentApplication.objects.filter(status='PENDING')
    return render(request, 'monitor/view_applications.html', {'applications': applications})


# ---------------------------APPROVE APPLICATION (MONITOR)---------------------------------


@login_required
def approve_application(request, id):
    if request.user.role != 'MONITOR':
        return redirect('login')

    application = StudentApplication.objects.get(id=id)
    application.status = 'APPROVED'
    application.save()

    profile = StudentProfile.objects.get(user=application.student)
    profile.is_approved = True
    profile.hostel = application.preferred_hostel
    profile.save()

    messages.success(request, "Application Approved Successfully")
    return redirect('view_applications')


# ----------------------REJECT APPLICATION (MONITOR)-------------------------------

@login_required
def reject_application(request, id):
    if request.user.role != 'MONITOR':
        return redirect('login')

    application = StudentApplication.objects.get(id=id)
    application.status = 'REJECTED'
    application.save()

    messages.error(request, "Application Rejected")
    return redirect('view_applications')


# ------------------------------------------------------------