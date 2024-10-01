from django.contrib.auth.models import User

# Get all user emails
user_emails = User.objects.values_list('email', flat=True).exclude(email='')

# Display the emails
for email in user_emails:
    print(email)

