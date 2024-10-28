import os
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from database.models import CreditHistory, Transaction, Moneylender, Borrower, Loan, ActiveLoan, Request
from database.serializers import CreditHistorySerializer, MoneylenderSerializer, BorrowerSerializer 
from database.serializers import LoansSerializer, RequestSerializer, TransactionSerializer, ActiveLoanSerializer, BorrowerLoanSerializer, MoneylenderRequestsSerializer
from django.contrib.auth.models import User
from llamascoin.serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework.exceptions import PermissionDenied
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_403_FORBIDDEN

# Create your views here.

#Vista de modelo para Borrower
class BorrowerViewSet(viewsets.ModelViewSet):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer

#Vista de modelo para Loans
class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()

    def get_serializer_class(self):
        # Seleccionar el serializer adecuado basado en el tipo de cuenta
        if hasattr(self.request.user, 'moneylender'):
            return LoansSerializer  # Serializer para Moneylender
        elif hasattr(self.request.user, 'borrower'):
            return BorrowerLoanSerializer  # Asegúrate de que tienes este serializer definido
        else:
            return LoansSerializer # Usa el serializer por defecto

    def list(self, request):
        # Comprobar si el usuario tiene el rol de Borrower
        if hasattr(request.user, 'borrower'):
            borrower = request.user.borrower  # Obtener el objeto Borrower del usuario autenticado
            
            # Obtener todos los préstamos
            loans = Loan.objects.all()
            
            # Serializar los préstamos y pasar el ID del Borrower en el contexto
            serializer = BorrowerLoanSerializer(loans, many=True, context={'borrower_id': borrower.id})
            return Response(serializer.data)
        
        # Si el usuario no es un Borrower, usa el serializer por defecto
        # y devuelve los prestmoas normalmente
        loans = Loan.objects.all()  
        serializer = LoansSerializer(loans, many=True)
        return Response(serializer.data)
    

    def create(self, request, *args, **kwargs):
        # Verificar si el usuario es un Moneylender
        # if not hasattr(request.user, 'moneylender'):
        #     raise PermissionDenied("No tienes permiso para crear un préstamo.")

        # Obtener el Moneylender asociado al usuario
        # moneylender = request.user.moneylender

        # # Verificar si is_subscribed es True
        # if not moneylender.is_subscribed:
        #     raise PermissionDenied("El Moneylender no está suscrito.")

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
    
    def retrieve(self, request, *args, **kwargs):
        # Obtener el usuario autenticado
        user = request.user

        try:
            moneylender = Moneylender.objects.get(user=user)
        except Moneylender.DoesNotExist:
            return Response({"detail": "Moneylender not found."}, status=HTTP_404_NOT_FOUND)
    
            # Verificar el estado de suscripción
        if not moneylender.is_subscribed:
            return Response({"detail": "Not subscribed."}, status=HTTP_403_FORBIDDEN)

        # Retornar el estado de suscripción si está suscrito
        return Response({"is_subscribed": True}, status=HTTP_200_OK)

class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    
    def get_queryset(self):
        # Filtrar según el tipo de cuenta del usuario
        if hasattr(self.request.user, 'moneylender'):
            # Si el usuario es un Moneylender, retornar solicitudes pendientes
            return Request.objects.filter(moneylender=self.request.user.moneylender, status='pending')
        elif hasattr(self.request.user, 'borrower'):
            # Si el usuario es un Borrower, retornar todas las solicitudes que le pertenecen
            return Request.objects.filter(borrower=self.request.user.borrower)
        else:
            # Si no tiene tipo de cuenta, retornamos un queryset vacío
            return Request.objects.none()  # No hay solicitudes para este usuario

    def get_serializer_class(self):
        # Seleccionar el serializer adecuado basado en el tipo de cuenta
        if hasattr(self.request.user, 'moneylender'):
            return MoneylenderRequestsSerializer
        else:
            return RequestSerializer  # Usa el serializer por defecto


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