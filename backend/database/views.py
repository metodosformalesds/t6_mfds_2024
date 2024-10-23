import os
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from database.models import CreditHistory, Transaction, Moneylender, Borrower, Loan
from database.serializers import CreditHistorySerializer, MoneylenderSerializer, BorrowerSerializer, LoansSerializer
# Create your views here.

#Vista de modelo para Borrower
class BorrowerViewSet(viewsets.ModelViewSet):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer

#Vista de modelo para Loans
class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoansSerializer

#Vista de modelo para money lender
class MoneylenderViewSet(viewsets.ModelViewSet):
    queryset = Moneylender.objects.all()
    serializer_class = MoneylenderSerializer

#Vista de modelo para credit history
class CreditHistoryViewSet(viewsets.ModelViewSet):
    queryset = CreditHistory.objects.all()
    serializer_class = CreditHistorySerializer

#Vista de modelo para end point Certificados de Facturas SAT
class SATCertificate(viewsets.modelEndPint):
    queryset = CreditHistory.objects.all()
    serializer_class = CreditHistorySerializer
