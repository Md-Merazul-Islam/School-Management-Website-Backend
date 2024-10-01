from rest_framework import serializers
from .models import Attendance, Mark

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
        
class MarkSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = Mark
        fields = ['id', 'student', 'student_name', 'subject', 'subject_name', 'marks', 'grade']

    def validate(self, data):
        student = data['student']
        subject = data['subject']

        # Check if the student already has marks for the subject
        if Mark.objects.filter(student=student, subject=subject).exists():
            raise serializers.ValidationError("Marks for this subject already exist for this student.")

        return data