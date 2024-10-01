from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Class(models.Model):
    SECTIONS = [('A', 'Section A'), ('B', 'Section B'), ('C', 'Section C'), ('D', 'Section D')]
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=1, choices=SECTIONS, default='A')

    def __str__(self):
        return f"{self.name} - {self.get_section_display()}"

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    code = models.CharField(max_length=6, unique=True)
    photo =  models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    
class Student(models.Model):
    roll_no = models.IntegerField(unique=True, editable=False, blank=True, null=True)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True) 
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    photo =  models.TextField(blank=True, null=True)
    class_name = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if not self.roll_no:
            last_student = Student.objects.order_by('-roll_no').first()
            self.roll_no = last_student.roll_no + 1 if last_student else 5000
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} - {self.roll_no} - {self.first_name} {self.last_name}"


class Teacher(models.Model):
    employee_id = models.IntegerField(unique=True, editable=False, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='teachers')
    photo =  models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.employee_id:
            last_teacher = Teacher.objects.order_by('-employee_id').first()
            self.employee_id = (last_teacher.employee_id + 1) if last_teacher else 1000
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.last_name} - {self.subject.name}"

    
    


class Notice(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    author =  models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) 
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('author',) 
    
    def __str__(self):
        if self.author:
            return f'Review by {self.author.username} for {self.created_at}'

