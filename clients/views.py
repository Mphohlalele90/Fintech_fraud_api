from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Client
from .utils import FraudDetector

@api_view(['POST'])
def loan_request(request):
    data = request.data
    
    # Validate required fields
    client_id = data.get("client_id")
    location = data.get("location")
    
    if not client_id or not location:
        return Response(
            {"error": "client_id and location are required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    # Get client from database
    try:
        client = Client.objects.get(client_id=client_id)
    except Client.DoesNotExist:
        return Response(
            {"error": "Client not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )

    # Extract optional fields
    transaction_time = data.get("transaction_time")
    current_imsi = data.get("device_imsi")
    current_number = data.get("device_number")

    # Perform fraud detection
    detector = FraudDetector()
    result = detector.assess_fraud_risk(
        client=client,
        location=location,
        transaction_time=transaction_time,
        current_imsi=current_imsi,
        current_number=current_number
    )

    # Build response
    response = {
    "client_id": client.client_id,
    "client_name": client.name,
    "approved": result["approved"],
    "flags": result["flags"],
    "risk_score": result["risk_score"],
    "risk_profile": result["risk_profile"],
    "message": result["message"]
}

    return Response(response)