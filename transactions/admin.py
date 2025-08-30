from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'loan_type', 'amount', 'risk_score', 'status', 'approved']
    list_filter = ['status', 'approved', 'loan_type', 'risk_profile']
    search_fields = ['client__client_id', 'device_imsi', 'device_number']