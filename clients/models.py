from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Client(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='clients')
    name = models.CharField(max_length=100, blank=True, null=True)
    client_id = models.CharField(max_length=20, unique=True)
    home_location = models.CharField(max_length=100)
    work_location = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    sim_swap = models.BooleanField(default=False)
    sim_swap_date = models.DateField(null=True, blank=True)
    imsi = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    risk_score = models.IntegerField(
        default=0, 
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    normal_activity_start = models.TimeField(default='08:00:00')
    normal_activity_end = models.TimeField(default='18:00:00')
    incident = models.CharField(max_length=200, blank=True, default='none')
    
    def __str__(self):
        return f"{self.client_id} - {self.user.get_full_name() or self.user.username}"
