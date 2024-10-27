from django.urls import path
from .views import PaymentSuccessView, PaymentFailView, PaymentCancelView, PaymentCreateView

urlpatterns = [
    path('success/', PaymentSuccessView.as_view(), name='payment_success'),
    path('fail/', PaymentFailView.as_view(), name='payment_fail'),
    path('cancel/', PaymentCancelView.as_view(), name='payment_cancel'),
    path('api/', PaymentCreateView.as_view(), name='payment'),
]
