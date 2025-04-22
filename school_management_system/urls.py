from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# 🔥 Swagger imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# 🔧 Swagger schema setup
schema_view = get_schema_view(
   openapi.Info(
      title="LMS",
      default_version='v1',
      description="API docs for School Management system",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="your@email.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include('accounts.urls')),
    path('academics/', include('academic.urls')),
    path('classes/', include('activites.urls')),
    path('payment/', include('payment.urls')),

    # 🚀 Swagger URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   
]

# 🖼 Media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
