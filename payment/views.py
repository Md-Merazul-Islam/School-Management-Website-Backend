from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from .serializers import PaymentSerializer


class PaymentCreateView(generics.CreateAPIView):
    """API view to create a new payment for school fees."""
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Handle POST request to create a payment."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment_data = serializer.create(serializer.validated_data)
        return Response(payment_data, status=status.HTTP_201_CREATED)

# Alternatively


class PaymentCreateCustomView(generics.CreateAPIView):
    """Custom API view to handle payment creation with additional logic."""
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Custom create method."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            payment_data = serializer.create(serializer.validated_data)
            return Response(payment_data, status=status.HTTP_201_CREATED)

        except serializers.ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": _("An unexpected error occurred.")}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
def PaymentSuccessView(request):
    return render(request, "success.html")


@csrf_exempt
def PaymentFailView(request):
    return render(request, "fail.html")

@csrf_exempt
def PaymentCancelView(request):
    return render(request, "cancel.html")
