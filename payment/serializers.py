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
        fields = ['id', 'tran_id', 'amount', 'cus_name',
                  'cus_email', 'cus_phone', 'month', 'user_id']
        read_only_fields = ['tran_id']

    def create(self, validated_data):
        """Create a new Payment instance for school fees and process payment."""
        try:
            # Extracting required fields
            amount = validated_data['amount']
            cus_name = validated_data['cus_name']
            cus_email = validated_data['cus_email']
            cus_phone = validated_data['cus_phone']
            month = validated_data['month']
            user_id = validated_data.get('user_id')

            with transaction.atomic():
                # Generate transaction ID
                transaction_id = self.generate_transaction_id()

                # Prepare data for AmarPay
                payload = {
                    "store_id": "aamarpaytest",
                    "tran_id": transaction_id,
                    "success_url": "https://amader-cst.netlify.app/payment-success/",
                    "fail_url": "https://school-management-five-iota.vercel.app/payment/fail/",
                    "cancel_url": "https://school-management-five-iota.vercel.app/payment/cancel/",
                    "amount": str(amount),
                    "currency": "BDT",
                    "signature_key": "dbb74894e82415a2f7ff0ec3a97e4183",
                    "desc": "School Fees Payment",
                    "cus_name": cus_name,
                    "cus_email": cus_email,
                    "cus_add1": "Dhaka , Bangladesh",
                    "cus_city": "Dhaka",
                    "cus_state": "Dhaka",
                    "cus_postcode": "1206",
                    "cus_country": "Bangladesh",
                    "cus_phone": cus_phone,
                    "type": "json"
                }

                # Make the request to AmarPay
                response = self.initiate_payment(payload)

                if response.get('result') == 'true':
                    gateway_url = response['payment_url']

                    # Create a Payment instance
                    payment = Payment.objects.create(
                        tran_id=transaction_id,
                        amount=amount,
                        cus_name=cus_name,
                        cus_email=cus_email,
                        cus_phone=cus_phone,
                        month=month,
                        user_id=user_id
                    )

                    return {
                        'cus_name': cus_name,
                        'month': month,
                        'cur_phone': cus_phone,
                        'payment_id': payment.id,
                        'payment_url': gateway_url,
                        'transaction_id': transaction_id
                    }
                else:
                    raise serializers.ValidationError(
                        {'error': _('Failed to create payment session')})

        except Exception as e:
            raise serializers.ValidationError(
                {'error': _('Failed to create payment: ' + str(e))})

    def initiate_payment(self, payload):
        """Initiate the payment with AmarPay."""
        url = "https://sandbox.aamarpay.com/jsonpost.php"
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            raise serializers.ValidationError(
                {'error': _('Failed to connect to AmarPay API.')})

    def generate_transaction_id(self):
        """Generate a unique transaction ID."""
        return f"txn-{str(uuid.uuid4())[:8]}"
