from django.db import models
from django.conf import settings
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Transaction(models.Model):
    LOAN_TYPES = [
        ('PERSONAL', 'Personal Loan'),
        ('BUSINESS', 'Business Loan'),
        ('EMERGENCY', 'Emergency Loan'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('UNDER_REVIEW', 'Under Review'),
    ]
    
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, related_name='transactions')
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_time = models.DateTimeField()
    location_lat = models.FloatField()
    location_long = models.FloatField()
    device_imsi = models.CharField(max_length=20)
    device_number = models.CharField(max_length=20)
    risk_score = models.IntegerField(
        default=0, 
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    risk_profile = models.CharField(max_length=20, default='LOW')
    flags = models.JSONField(default=list)  # Stores list of fraud flags
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    approved = models.BooleanField(default=False)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Transaction {self.id} - {self.client.client_id}"