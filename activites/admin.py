from django.contrib import admin
from .models import Attendance, Mark

# @admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('roll_no', 'date', 'status') 

admin.site.register(Attendance, AttendanceAdmin)

@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'marks', 'grade')
    search_fields = ('student__first_name', 'student__last_name', 'subject__name')
    list_filter = ('subject', 'grade')
    ordering = ('student', 'subject')
