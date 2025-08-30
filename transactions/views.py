from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Transaction
from .serializers import TransactionSerializer
from .fraud_detector import FraudDetector

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own transactions
        return Transaction.objects.filter(client__user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        # Import here to avoid circular imports
        from clients.models import Client
        
        client = get_object_or_404(Client, user=request.user)
        
        # Analyze for fraud
        fraud_analysis = FraudDetector.analyze_transaction(client, request.data)
        
        # Create transaction with fraud analysis results
        transaction_data = {
            **request.data,
            'client': client.id,
            'risk_score': fraud_analysis['risk_score'],
            'risk_profile': fraud_analysis['risk_profile'],
            'flags': fraud_analysis['flags'],
            'approved': fraud_analysis['approved'],
            'message': fraud_analysis['message'],
            'status': 'APPROVED' if fraud_analysis['approved'] else 'REJECTED'
        }
        
        serializer = self.get_serializer(data=transaction_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=['post'])
    def manual_review(self, request, pk=None):
        transaction = self.get_object()
        if transaction.status != 'REJECTED':
            return Response(
                {"error": "Only rejected transactions can be sent for manual review"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        transaction.status = 'UNDER_REVIEW'
        transaction.save()
        
        return Response({
            "message": "Transaction sent for manual review",
            "transaction_id": transaction.id,
            "status": transaction.status
        })