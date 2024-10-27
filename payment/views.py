from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # Import if you want to restrict access to authenticated users
from .models import Payment
from .serializers import PaymentSerializer

class PaymentCreateView(generics.CreateAPIView):
    """API view to create a new payment for school fees."""
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]  # Restrict to authenticated users, if needed

    def post(self, request, *args, **kwargs):
        """Handle POST request to create a payment."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Validate the incoming data
        
        # Create payment and initiate the payment session
        payment_data = serializer.create(serializer.validated_data)
        
        return Response(payment_data, status=status.HTTP_201_CREATED)

# Alternatively, if you want to have more detailed control or custom logic, 
# you can override the create method directly in the view.

class PaymentCreateCustomView(generics.CreateAPIView):
    """Custom API view to handle payment creation with additional logic."""
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]  # Restrict to authenticated users, if needed

    def create(self, request, *args, **kwargs):
        """Custom create method."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Create payment and get the response
            payment_data = serializer.create(serializer.validated_data)
            return Response(payment_data, status=status.HTTP_201_CREATED)
        
        except serializers.ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": _("An unexpected error occurred.")}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from django.shortcuts import render
from django.views import View
class PaymentSuccessView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "success.html")


class PaymentFailView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "fail.html")


class PaymentCancelView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "cancel.html")


# {
#     "user_id": 5,
#     "amount": 500,
#     "month_name": "October"
# }
