from django.urls import path
from . import views

urlpatterns = [
    path('loan/request/', views.loan_request, name='loan-request'),
]