from django.contrib import admin
from .models import User, Hostel, Room, StudentApplication, StudentProfile


admin.site.register(User)
admin.site.register(Hostel)
admin.site.register(Room)
admin.site.register(StudentApplication)
admin.site.register(StudentProfile)