from rest_framework import viewsets
from .models import Student, Teacher, Class, Subject, Review
from .serializers import StudentSerializer, TeacherSerializer, ClassSerializer, SubjectSerializer, ReviewSerializer,StudentSerializerForList
from .permissions import IsAdminOrReadOnly
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TeacherFilter, StudentFilter
from .models import Notice
from .serializers import NoticeSerializer
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
import datetime
from django.conf import settings
import logging

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    # permission_classes = [IsAdminOrReadOnly]  #  custom permission


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    # permission_classes = [IsAdminOrReadOnly]  #  custom permission

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    # permission_classes = [IsAdminOrReadOnly]  #  custom permission

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    # permission_classes = [IsAdminOrReadOnly]  # custom permission
    

# This is for filtering only, no POST allowed 
class StudentListView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializerForList
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentFilter
    

class TeacherListView(generics.ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TeacherFilter
    
    
    
    

import logging
import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Notice
from .serializers import NoticeSerializer
from django.conf import settings
from django.contrib.auth.models import User


logger = logging.getLogger(__name__)

class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all().order_by('-created_at')
    serializer_class = NoticeSerializer
    
    def perform_create(self, serializer):
        notice = serializer.save()
        active_user_emails = User.objects.filter(is_active=True).values_list('email', flat=True).exclude(email='')

        email_subject = "Important Notice: " + notice.title
        context = {
            'title': notice.title,
            'description': notice.description,
            'file_url': notice.image,  
            'current_year': datetime.datetime.now().year
        }
        email_body = render_to_string('notice_email.html', context)

        for email in active_user_emails:
            try:
                email_message = EmailMultiAlternatives(
                    subject=email_subject,
                    body='', 
                    from_email=settings.EMAIL_HOST_USER,
                    to=[email]
                )
                email_message.attach_alternative(email_body, "text/html")
                email_message.send()
            except Exception as e:
                logger.error(f"Error sending email to {email}: {e}")

        return Response({'message': 'Successfully sent email and notice updated.'}, status=200)



from rest_framework.permissions import BasePermission, SAFE_METHODS
class IsAuthenticatedOrReadOnlyForReview(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnlyForReview] 
    
    
   

