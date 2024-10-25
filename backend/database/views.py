import os
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from database.models import CreditHistory, Transaction, Moneylender, Borrower, Loan, ActiveLoan
from database.serializers import CreditHistorySerializer, MoneylenderSerializer, BorrowerSerializer 
from database.serializers import LoansSerializer, RequestSerializer, TransactionSerializer, ActiveLoanSerializer
from django.contrib.auth.models import User
from llamascoin.serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework.exceptions import PermissionDenied

# Create your views here.

#Vista de modelo para Borrower
class BorrowerViewSet(viewsets.ModelViewSet):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer

#Vista de modelo para Loans
class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoansSerializer
    
    def create(self, request, *args, **kwargs):
        # Verificar si el usuario es un Moneylender
        if not hasattr(request.user, 'moneylender'):
            raise PermissionDenied("No tienes permiso para crear un préstamo.")

        # Obtener el Moneylender asociado al usuario
        moneylender = request.user.moneylender

        # Verificar si is_subscribed es True
        if not moneylender.is_subscribed:
            raise PermissionDenied("El Moneylender no está suscrito.")

        # Si todas las verificaciones son satisfactorias, proceder a crear el préstamo
        return super().create(request, *args, **kwargs)

#Vista de modelo para money lender
class MoneylenderViewSet(viewsets.ModelViewSet):
    queryset = Moneylender.objects.all()
    serializer_class = MoneylenderSerializer

#Vista de modelo para credit history
class CreditHistoryViewSet(viewsets.ModelViewSet):
    queryset = CreditHistory.objects.all()
    serializer_class = CreditHistorySerializer

#Vista de modelo para ver usuarios registrados
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RequestViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RequestSerializer
    
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    
class ActiveLoanViewSet(viewsets.ModelViewSet):
    queryset = ActiveLoan.objects.all()
    serializer_class = ActiveLoanSerializer
    
def register_routers():
    """
    Función para registrar múltiples routers.
    """
    # Lista de viewsets con sus respectivos basenames
    viewsets_with_basenames = [
        ('credit_history', CreditHistoryViewSet),
        ('moneylender', MoneylenderViewSet),
        ('borrower', BorrowerViewSet),
        ('loan', LoanViewSet),
        ('user', UserViewSet),
        ('request', RequestViewSet),
        ('transaction', TransactionViewSet),
        ('active_loan', ActiveLoanViewSet)
    ]
    routers = {}
    for basename, viewset in viewsets_with_basenames:
        router = DefaultRouter()
        router.register(r'', viewset, basename=basename)
        routers[basename] = router
        
    return routers