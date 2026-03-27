from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User

from .models import *
from .forms import *
from django.contrib import messages

from django.shortcuts import get_object_or_404



# --------------------TRY VIEWS-------------------

def check(request):
    return render(request, 'student/apply_hostel.html')

# -----------------HOME --------------------

def home(request):
    hostels = Hostel.objects.all()[:10] # campuses
    return render(request, 'home.html', {'hostels': hostels})


# ---------------- LOGIN ----------------

def login(request):
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
def warden_dashboard(request):
    return render(request, 'warden/dashboard.html')



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

    user = get_object_or_404(User, id=user_id)

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

    monitor = get_object_or_404(Monitor, id=id)
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

    profile = StudentProfile.objects.get(user=request.user)

    if not profile.is_approved:
        return render(request, 'student/pending.html')

    return render(request, 'student/dashboard.html')

# ---------------- STUDENT REGISTER ---------------------

def student_register(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)

        if form.is_valid():
            # Create User
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                role='STUDENT'
            )

            # Create Student Profile
            profile = StudentProfile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                dob=form.cleaned_data['dob'],
                gender=form.cleaned_data['gender'],
                address=form.cleaned_data['address'],
                contact=form.cleaned_data['contact'],
                course=form.cleaned_data['course'],
                college_name=form.cleaned_data['college_name'],
                college_year=form.cleaned_data['college_year']
            )

            # Create Hostel Application
            StudentApplication.objects.create(
                student=profile,  # (make sure you updated model)
                preferred_hostel=form.cleaned_data['preferred_hostel']
            )

            messages.success(request, "Registration successful! Please login.")
            return redirect('login')

    else:
        form = StudentRegisterForm()

    return render(request, 'student/register.html', {'form': form})


# ---------------- VIEW HOSTELS (STUDENT) ----------------

@login_required
def student_view_hostels(request):
    if request.user.role != 'STUDENT':
        return redirect('login')

    hostels = Hostel.objects.all()
    return render(request, 'student/view_hostels.html', {'hostels': hostels})



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

    application = get_object_or_404(StudentApplication, id=id)
    hostels = Hostel.objects.all()

    hostel_data = []

    for hostel in hostels:
        rooms = Room.objects.filter(hostel=hostel)

        total_capacity = sum(room.capacity for room in rooms)
        total_occupied = sum(room.occupied for room in rooms)
        available = total_capacity - total_occupied

        hostel_data.append({
            'hostel': hostel,
            'total_capacity': total_capacity,
            'occupied': total_occupied,
            'available': available
        })

    if request.method == 'POST':
        hostel_id = request.POST.get('hostel_id')
        selected_hostel = Hostel.objects.get(id=hostel_id)

        # Update application
        rooms = Room.objects.filter(hostel=selected_hostel)
        total_capacity = sum(room.capacity for room in rooms)
        total_occupied = sum(room.occupied for room in rooms)

        if total_occupied >= total_capacity:
            messages.error(request, "Hostel is Full")
            return redirect('view_applications')

        # approve after check
        application.status = 'APPROVED'
        application.assigned_hostel = selected_hostel
        application.save()

        profile = application.student
        profile.is_approved = True
        profile.hostel = selected_hostel
        profile.save()

        messages.success(request, "Hostel Assigned & Application Approved")
        return redirect('view_applications')

    return render(request, 'monitor/approve_application.html', {
        'application': application,
        'hostel_data': hostel_data

    })


# ----------------------REJECT APPLICATION (MONITOR)-------------------------------

@login_required
def reject_application(request, id):
    if request.user.role != 'MONITOR':
        return redirect('login')

    application = get_object_or_404(StudentApplication, id=id)
    application.status = 'REJECTED'
    application.save()

    messages.error(request, "Application Rejected")
    return redirect('view_applications')


# -----------------------monitor assign room-------------------------------------