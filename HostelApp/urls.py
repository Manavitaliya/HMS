from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('redirect/', views.redirect_dashboard, name='redirect_dashboard'),
    path('check/', views.check, name = 'check'),

    # Admin
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/create-hostel/', views.create_hostel, name='create_hostel'),
    path('admin/view-hostels/', views.view_hostels, name='view_hostels'),
    path('admin/create-monitor/', views.create_monitor, name='create_monitor'),
    path('admin/create-warden/', views.create_warden, name='create_warden'),
    path('admin/assign-warden/<int:user_id>/', views.assign_warden, name='assign_warden'),
    path('admin/view-monitors/', views.view_monitors, name='view_monitors'),
    path('admin/view-wardens/', views.view_wardens, name='view_wardens'),
    path('admin/delete-monitor/<int:id>/', views.delete_monitor, name='delete_monitor'),
    path('admin/delete-warden/<int:id>/', views.delete_warden, name='delete_warden'),

    # Student
    path('student/register/', views.student_register, name='student_register'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/apply/', views.apply_hostel, name='apply_hostel'),

    # Monitor
    path('monitor/dashboard/', views.monitor_dashboard, name='monitor_dashboard'),
    path('monitor/applications/', views.view_applications, name='view_applications'),
    
    path('monitor/applications/', views.all_applications, name='all_applications'),
    path('monitor/applications/<str:status>/', views.filtered_applications, name='filtered_applications'),

    # Application detail
    path('monitor/application/<int:id>/', views.application_detail, name='application_detail'),


    path('monitor/approve/<int:id>/', views.approve_application, name='approve_application'),
    path('monitor/reject/<int:id>/', views.reject_application, name='reject_application'),

    # Warden
    path('warden/dashboard/', views.warden_dashboard, name='warden_dashboard'),
]

