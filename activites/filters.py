
from django_filters import rest_framework as filters
from .models import Attendance
from .serializers import AttendanceSerializer

class AttendanceFilter(filters.FilterSet):
    
    date = filters.DateFilter(field_name='date', lookup_expr='exact')
    status = filters.ChoiceFilter(field_name='status', choices=Attendance.STATUS_CHOICES)

    class Meta:
        model = Attendance
        fields = ['date', 'status']
