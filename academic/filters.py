from django_filters import rest_framework as filters
from .models import Teacher,Student

class TeacherFilter(filters.FilterSet):
    email = filters.CharFilter(field_name='email', lookup_expr='icontains')
    subject = filters.NumberFilter(field_name='subject')
    employee_id = filters.NumberFilter(field_name='employee_id')

    class Meta:
        model = Teacher
        fields = ['employee_id', 'email', 'subject']



class StudentFilter(filters.FilterSet):
    first_name = filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    username = filters.CharFilter(field_name='username', lookup_expr='icontains')
    roll_no = filters.NumberFilter(field_name='roll_no')

    class Meta:
        model = Student
        fields = ['first_name','username', 'roll_no']
        