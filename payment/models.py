# models.py
from django.db import models
from django.utils import timezone
import uuid

class Payment(models.Model):
    MONTH_CHOICES = [
        ('JAN', 'January'),
        ('FEB', 'February'),
        ('MAR', 'March'),
        ('APR', 'April'),
        ('MAY', 'May'),
        ('JUN', 'June'),
        ('JUL', 'July'),
        ('AUG', 'August'),
        ('SEP', 'September'),
        ('OCT', 'October'),
        ('NOV', 'November'),
        ('DEC', 'December'),
    ]

    tran_id = models.CharField(max_length=32, unique=True, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    cus_name = models.CharField(max_length=255)
    cus_email = models.EmailField()
    cus_phone = models.CharField(max_length=15)
    month = models.CharField(max_length=3, choices=MONTH_CHOICES) 
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.tran_id:  # Generate tran_id only if it's not already set
            unique_id = str(uuid.uuid4())[:8]  # Generate a unique ID (first 8 characters)
            self.tran_id = f"{self.month}-{unique_id}"  # Combine month and unique ID
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tran_id} - {self.cus_name} - {self.month}"
