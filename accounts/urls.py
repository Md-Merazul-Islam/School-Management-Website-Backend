from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProfileViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='all_user')
router.register(r'profiles', ProfileViewSet, basename='user_info')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.UserRegistrationSerializerViewSet.as_view(), name='register'),
    # path('active/<uid64>/<token>/', views.activate, name='active'),
    path('active/<str:uid64>/<str:token>/', views.activate, name='active'),
    path('login/', views.UserLoginApiView.as_view(), name='login'),
    path('logout/', views.UserLogoutApiView.as_view(), name='logout'),
    path('successful-email-verified/', views.successful, name='verified_success'),
    path('unsuccessful-email-verified/',
         views.unsuccessful, name='verified_failed'),
    path('user-profile-update/',
         views.UserProfileView.as_view(), name='update_profile')
]
