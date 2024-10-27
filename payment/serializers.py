# serializers.py
from rest_framework import serializers
from .models import Payment
from django.db import transaction
from django.utils.translation import gettext as _
import requests
import json
import uuid

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'tran_id', 'amount', 'cus_name', 'cus_email', 'cus_phone', 'month', 'user_id']
        read_only_fields = ['tran_id']  # tran_id should be read-only since it is generated

    def create(self, validated_data):
        """Create a new Payment instance for school fees and process payment."""
        try:
            # Extracting required fields
            amount = validated_data['amount']
            cus_name = validated_data['cus_name']
            cus_email = validated_data['cus_email']
            cus_phone = validated_data['cus_phone']
            month = validated_data['month']
            user_id = validated_data.get('user_id')  # User ID associated with the payment

            with transaction.atomic():
                # Generate transaction ID
                transaction_id = self.generate_transaction_id()

                # Prepare data for AmarPay
                payload = {
                    "store_id": "aamarpaytest",  # Replace with your actual store ID
                    "tran_id": transaction_id,
                    "success_url": "http://127.0.0.1:8000/payment/success/",
                    "fail_url": "http://127.0.0.1:8000/payment/fail/",
                    "cancel_url": "http://127.0.0.1:8000/payment/cancel/",
                    "amount": str(amount),  # Amount as string
                    "currency": "BDT",
                    "signature_key": "dbb74894e82415a2f7ff0ec3a97e4183",  # Replace with your actual signature key
                    "desc": "School Fees Payment",
                    "cus_name": cus_name,
                    "cus_email": cus_email,
                    "cus_add1": "User Address Here",  # Adjust accordingly
                    "cus_city": "Dhaka",  # Adjust accordingly
                    "cus_state": "Dhaka",
                    "cus_postcode": "1206",  # Adjust accordingly
                    "cus_country": "Bangladesh",
                    "cus_phone": cus_phone,
                    "type": "json"
                }

                # Make the request to AmarPay
                response = self.initiate_payment(payload)

                if response.get('result') == 'true':
                    gateway_url = response['payment_url']  # Extract payment URL from the response

                    # Create a Payment instance
                    payment = Payment.objects.create(
                        tran_id=transaction_id,
                        amount=amount,
                        cus_name=cus_name,
                        cus_email=cus_email,
                        cus_phone=cus_phone,
                        month=month,
                        user_id=user_id  # Assuming user_id can be passed in
                    )

                    return {
                        'payment_id': payment.id,  # You can return the payment ID if needed
                        'payment_url': gateway_url,
                        'transaction_id': transaction_id
                    }
                else:
                    raise serializers.ValidationError({'error': _('Failed to create payment session')})

        except Exception as e:
            raise serializers.ValidationError({'error': _('Failed to create payment: ' + str(e))})

    def initiate_payment(self, payload):
        """Initiate the payment with AmarPay."""
        url = "https://sandbox.aamarpay.com/jsonpost.php"  # Sandbox URL for testing
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()  # Assuming the response is in JSON format
        else:
            raise serializers.ValidationError({'error': _('Failed to connect to AmarPay API.')})

    def generate_transaction_id(self):
        """Generate a unique transaction ID."""
        return f"txn-{str(uuid.uuid4())[:8]}"  # Generate a simple transaction ID
