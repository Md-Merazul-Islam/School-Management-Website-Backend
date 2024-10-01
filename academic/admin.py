from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Student, Teacher, Class, Subject, Notice, Review

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('username', 'roll_no', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'photo', 'class_name')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'address')
    list_filter = ('class_name',)
    ordering = ('roll_no',)
    
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'first_name', 'last_name', 'email', 'subject')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('subject',)
    ordering = ('employee_id',)

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'section')
    search_fields = ('name',)
    list_filter = ('section',)
    ordering = ('name',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'code')
    search_fields = ('name', 'code')
    ordering = ('name',)



admin.site.register(Notice)
admin.site.register(Review)