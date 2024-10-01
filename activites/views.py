from rest_framework import viewsets
from .models import Attendance, Mark
from .serializers import AttendanceSerializer, MarkSerializer
from django_filters import rest_framework as filters
from.filters import AttendanceFilter
from .permissions import IsStaffOrReadOnly
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AttendanceFilter
    # permission_classes = [IsStaffOrReadOnly]  #  custom permission


class MarkViewSet(viewsets.ModelViewSet):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer

    def get_queryset(self):
        queryset = Mark.objects.all()
        student_id = self.request.query_params.get('student', None)
        subject_id = self.request.query_params.get('subject', None)

        if student_id:
            queryset = queryset.filter(student__id=student_id)
        if subject_id:
            queryset = queryset.filter(subject__id=subject_id)

        return queryset



class AttendanceListCreateView(generics.ListCreateAPIView):
    serializer_class = AttendanceSerializer
    # permission_classes = [IsStaffOrReadOnly]  #  custom permission

    def get_queryset(self):
        roll_no = self.request.query_params.get('roll_no', None)
        if roll_no:
            return Attendance.objects.filter(roll_no=roll_no, date=timezone.now().date())
        return Attendance.objects.filter(date=timezone.now().date())

    def post(self, request, *args, **kwargs):
        roll_no = request.data.get('roll_no')
        if not roll_no:
            return Response({"error": "Roll number is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        existing_attendance = Attendance.objects.filter(roll_no=roll_no, date=timezone.now().date()).first()
        if existing_attendance:
            return Response({"error": "Attendance already recorded for today."}, status=status.HTTP_400_BAD_REQUEST)

        return self.create(request, *args, **kwargs)
