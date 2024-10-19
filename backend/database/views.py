import os
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from database.models import CreditHistory, Transaction, Moneylender
from database.serializers import CreditHistorySerializer, MoneylenderSerializer
# Create your views here.


#Vista de modelo para money lender
class MoneylenderViewSet(viewsets.ModelViewSet):
    queryset = Moneylender.objects.all()
    serializer_class = MoneylenderSerializer

#Vista de modelo para credit history
class CreditHistoryViewSet(viewsets.ModelViewSet):
    queryset = CreditHistory.objects.all()
    serializer_class = CreditHistorySerializer
