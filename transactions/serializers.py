from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('risk_score', 'risk_profile', 'flags', 'status', 'approved', 'message', 'created_at')