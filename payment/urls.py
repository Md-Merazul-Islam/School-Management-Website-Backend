from django.urls import path
from .views import PaymentSuccessView, PaymentFailView, PaymentCancelView, PaymentCreateView, PaymentCreateCustomView

urlpatterns = [
    path('api/', PaymentCreateView.as_view(), name='payment'),
    path('api2/', PaymentCreateCustomView.as_view(), name='payment_api2'),
    path('success/', PaymentSuccessView, name='payment_success'),
    path('fail/', PaymentFailView, name='payment_fail'),
    path('cancel/', PaymentCancelView, name='payment_cancel'),
]
