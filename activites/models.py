from django.db import models
from academic.models import Student, Subject
from .utils import send_sms, send_email
from django.utils import timezone

class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    grade = models.CharField(max_length=2, editable=False)
    
    class Meta:
        unique_together = ('student', 'subject') 


    def save(self, *args, **kwargs):
        self.grade = self.calculate_grade(self.marks)
        super().save(*args, **kwargs)

    def calculate_grade(self, marks):
        if marks >= 90: return 'A+'
        elif marks >= 80: return 'A'
        elif marks >= 70: return 'B+'
        elif marks >= 60: return 'B'
        elif marks >= 50: return 'C+'
        elif marks >= 40: return 'C'
        else: return 'F'

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.grade}"



class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent')
    ]
    
    roll_no = models.IntegerField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Absent')
    
    class Meta:
        unique_together = ('roll_no', 'date')
    
    def __str__(self):
        return f"Roll No: {self.roll_no} - {self.date} - {self.status}"
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.status == 'Absent':
            print(f"Attendance marked as Absent for roll_no {self.roll_no}. Sending notifications...")
            try:
                student = Student.objects.get(roll_no=self.roll_no)
                parent_phone_number = student.phone_number
                parent_email = student.email
                
                if parent_phone_number:
                    message = f"Alert: Your child {student.first_name} {student.last_name} was marked absent on {self.date}."
                    send_sms(parent_phone_number, message)
                
                if parent_email:
                    context = {
                        'student': student,
                        'date': self.date,
                    }
                    send_email(parent_email, 'Absence Notification', 'notifications/absent_notification.html', context)
                    
            except Student.DoesNotExist:
                print(f"No student found with roll_no {self.roll_no}")


