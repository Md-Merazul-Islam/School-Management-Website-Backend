from twilio.rest import Client
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import phonenumbers
from phonenumbers import parse, is_valid_number, format_number, PhoneNumberFormat
from phonenumbers.phonenumberutil import NumberParseException

def send_email(to_email, subject, template_name, context):
    email_body = render_to_string(template_name, context)
    email = EmailMultiAlternatives(
        subject=subject,
        body='',
        to=[to_email]
    )
    email.attach_alternative(email_body, "text/html")
    email.send()

def format_phone_number(phone_number):
    try:
        parsed_number = parse(phone_number, "BD") 
        if is_valid_number(parsed_number):
            return format_number(parsed_number, PhoneNumberFormat.E164)
        else:
            raise ValueError("Invalid phone number")
    except NumberParseException:
        raise ValueError("Invalid phone number format")

def send_sms(phone_number, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    try:
        formatted_number = format_phone_number(phone_number)
        client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,  
            to=formatted_number
        )
    except Exception as e:
        print(f"Failed to send SMS: {e}")
