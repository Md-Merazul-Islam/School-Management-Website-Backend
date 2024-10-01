from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, TeacherViewSet, ClassViewSet, SubjectViewSet, StudentListView, TeacherListView, NoticeViewSet,ReviewViewSet
router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'notices', NoticeViewSet, basename='notice')
router.register(r'reviews', ReviewViewSet, basename='review_view')


urlpatterns = [
    path('', include(router.urls)),
    path('students-list/', StudentListView.as_view(), name='student-list'),
    path('teachers-list/', TeacherListView.as_view(), name='teacher-list'),
]
