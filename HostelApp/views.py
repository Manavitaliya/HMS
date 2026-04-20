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
    return render(request, 'student/dashboard.html')

# -----------------HOME --------------------

def home(request):
    hostels = Hostel.objects.all()[:10] # campuses
    return render(request, 'home.html', {'hostels': hostels})

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
    return redirect('home')


# -----------------------------------------------------------------
# --------------- STUDENT PANNEL-----------------------------------
# -----------------------------------------------------------------

# >>>>>> STUDENT REGISTRATION <<<<<<

def student_register(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                role='STUDENT'
            )

            messages.success(request, "Registration successful! Please login.")
            return redirect('login')
        else:
            print(form.errors) 
    else:
        form = StudentRegisterForm()

    return render(request, 'student/register.html', {'form': form})


# >>>>> STUDENT DASHBOARD<<<<<

@login_required
def student_dashboard(request):

    hostels = Hostel.objects.all()

    profile = StudentProfile.objects.filter(user=request.user).first()

    if not profile:
        return render(request, 'student/dashboard.html', {
            'no_profile': True}, {'hostels': hostels})

    application = StudentApplication.objects.filter(student=profile).last()

    if application.status == 'PENDING':
        return render(request, 'student/dashboard.html', {
            'pending': True, 'hostels': hostels
        })

    elif application.status == 'REJECTED':
        return render(request, 'student/dashboard.html', {
            'rejected': True, 'hostels': hostels
        })

    elif application.status == 'APPROVED':
        return render(request, 'student/dashboard.html', {
            'approved': True,
            'profile': profile, 'hostels': hostels
        })


# >>>>> APPLY HOSTEL <<<<<

from datetime import datetime

@login_required
def apply_hostel(request):
    if request.user.role != 'STUDENT':
        return redirect('login')

    # Prevent multiple active applications
    existing_application = StudentApplication.objects.filter(
        student__user=request.user,
        status='PENDING'
    ).first()

    if existing_application:
        messages.warning(request, "You already have a pending application")
        return redirect('student_dashboard')

    hostels = Hostel.objects.all()

    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')

        full_name = f"{first_name} {middle_name} {last_name}"

        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        course = request.POST.get('course')
        college_name = request.POST.get('college_name')
        college_year = request.POST.get('college_year')

        hostel_id = request.POST.get('preferred_hostel')
        preferred_hostel = Hostel.objects.get(id=hostel_id)

        # Create Profile (IMPORTANT: only here profile created)
        profile = StudentProfile.objects.create(
            user=request.user,
            full_name=full_name,
            dob=dob,
            gender=gender,
            contact=contact,
            address=address,
            course=course,
            college_name=college_name,
            college_year=college_year
        )

        # Create Application
        StudentApplication.objects.create(
            student=profile,
            preferred_hostel=preferred_hostel
        )

        messages.success(request, "Application Submitted Successfully")
        return redirect('student_dashboard')

    return render(request, 'student/apply_hostel.html', {'hostels': hostels})


# -----------------------------------------------------------------
# --------------- MONITOR PANNEL-----------------------------------
# -----------------------------------------------------------------

# >>>>> MONITOR DASHBORAD <<<<<

@login_required
def monitor_dashboard(request):
    if request.user.role != 'MONITOR':
        return redirect('login')

    applications = StudentApplication.objects.select_related(
        'student', 'preferred_hostel'
    )

    # FILTER
    status = request.GET.get('status')
    hostel_id = request.GET.get('hostel')

    if status:
        applications = applications.filter(status=status)

    if hostel_id:
        applications = applications.filter(preferred_hostel_id=hostel_id)

    # HOSTEL AVAILABILITY
    hostel_data = []
    hostels = Hostel.objects.all()

    for hostel in hostels:
        beds = Bed.objects.filter(room__hostel=hostel)
        total = beds.count()
        occupied = beds.filter(is_occupied=True).count()

        hostel_data.append({
            'hostel': hostel,
            'available': total - occupied,
            'occupied': occupied
        })

    context = {
        'total': StudentApplication.objects.count(),
        'pending': StudentApplication.objects.filter(status='PENDING').count(),
        'approved': StudentApplication.objects.filter(status='APPROVED').count(),
        'rejected': StudentApplication.objects.filter(status='REJECTED').count(),
        'applications': applications.order_by('-applied_at')[:10],
        'hostel_data': hostel_data,
        'hostels': hostels
    }

    return render(request, 'monitor/dashboard.html', context)

# >>>>> VIEW APPLICATIONS <<<<<

@login_required
def view_applications(request):
    if request.user.role != 'MONITOR':
        return redirect('login')

    applications = StudentApplication.objects.select_related(
        'student', 'preferred_hostel'
    ).filter(status='PENDING').order_by('-applied_at')

    return render(request, 'monitor/view_applications.html', {
        'applications': applications
    })
    
    
# >>>>> APPROVE APPLICATIONS <<<<<

@login_required
def approve_application(request, id):
    if request.user.role != 'MONITOR':
        return redirect('login')

    application = get_object_or_404(StudentApplication, id=id)

    hostels = Hostel.objects.all()

    hostel_data = []

    for hostel in hostels:
        rooms = Room.objects.filter(hostel=hostel)
        beds = Bed.objects.filter(room__hostel=hostel)

        total_beds = beds.count()
        occupied_beds = beds.filter(is_occupied=True).count()
        available_beds = total_beds - occupied_beds

        hostel_data.append({
            'hostel': hostel,
            'total_beds': total_beds,
            'occupied': occupied_beds,
            'available': available_beds
        })

    if request.method == 'POST':
        hostel_id = request.POST.get('hostel_id')
        selected_hostel = get_object_or_404(Hostel, id=hostel_id)

        # Check availability again (IMPORTANT)
        beds = Bed.objects.filter(room__hostel=selected_hostel)
        if beds.filter(is_occupied=False).count() == 0:
            messages.error(request, "Hostel is Full")
            return redirect('view_applications')

        # APPROVE
        application.status = 'APPROVED'
        application.assigned_hostel = selected_hostel
        application.save()

        # Update student profile
        profile = application.student
        profile.hostel = selected_hostel
        profile.save()

        messages.success(request, "Application Approved & Hostel Assigned")
        return redirect('view_applications')

    return render(request, 'monitor/approve_application.html', {
        'application': application,
        'hostel_data': hostel_data
    })
    
    
# >>>>> REJECT APPLICATIONS <<<<<

@login_required
def reject_application(request, id):
    if request.user.role != 'MONITOR':
        return redirect('login')

    application = get_object_or_404(StudentApplication, id=id)

    application.status = 'REJECTED'
    application.save()

    messages.error(request, "Application Rejected")
    return redirect('view_applications')


# >>>>>>
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
