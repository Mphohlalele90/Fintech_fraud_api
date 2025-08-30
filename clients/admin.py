from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['client_id', 'user', 'phone_number', 'risk_score', 'sim_swap']
    list_filter = ['sim_swap', 'risk_score']
    search_fields = ['client_id', 'user__username', 'phone_number']