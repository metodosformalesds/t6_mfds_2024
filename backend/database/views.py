import os
from django.utils import timezone
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from services.Score.score import calcular_dificultad
from database.models import CreditHistory, Payments, Transaction, Moneylender, Borrower, Loan, ActiveLoan, Request
from database.serializers import BorrowerActiveLoanSerializer, CreditHistorySerializer, MoneylenderSerializer, BorrowerSerializer, MoneylenderLoanSerializer, BorrowerRequestSerializer, PaymentSerializer, MoneylenderDetailSerializer
from database.serializers import LoansSerializer, RequestSerializer, TransactionSerializer, ActiveLoanSerializer, BorrowerLoanSerializer, MoneylenderRequestsSerializer, BorrowerCreditHistorySerializer, MoneylenderTransactionSerializer
from django.contrib.auth.models import User
from llamascoin.serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework.exceptions import PermissionDenied
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from django.contrib.auth import get_user_model
# Create your views here.

#Vista de modelo para Borrower
class BorrowerViewSet(viewsets.ModelViewSet):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer

    def retrieve(self, request, *args, **kwargs):
        borrower_id = kwargs.get('pk')

        if hasattr(request.user, 'borrower'):
            # Borrower accediendo a su propio historial
            borrower = get_object_or_404(Borrower, user=request.user)
            serializer = BorrowerCreditHistorySerializer(borrower)
            return Response(serializer.data, status=HTTP_200_OK)
        
        elif hasattr(request.user, 'moneylender'):
            # Moneylender accediendo al historial de un borrower específico
            borrower = get_object_or_404(Borrower, id=borrower_id)
            serializer = BorrowerCreditHistorySerializer(borrower)
            return Response(serializer.data, status=HTTP_200_OK)

        return Response({"detail": "No tienes permiso para acceder a esta información."}, status=HTTP_403_FORBIDDEN)
    
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
            
            # Intentar obtener el ActiveLoan del Borrower si existe
            active_loan = ActiveLoan.objects.filter(borrower=borrower, amount_to_pay__gt=0).first()
            
            # Si existe un ActiveLoan con `amount_to_pay > 0`
            if active_loan:
                active_loan_serializer = BorrowerActiveLoanSerializer(active_loan)
                response_data = {
                    'active_loan': active_loan_serializer.data
                }
                return Response(response_data, status=HTTP_200_OK)
            
            # Si no hay ActiveLoan pendiente, obtener todos los préstamos
            loans = Loan.objects.all()
            loans_serializer = BorrowerLoanSerializer(loans, many=True, context={'borrower_id': borrower.id})
            
            # Construir la respuesta con todos los préstamos
            response_data = {
                'loans': loans_serializer.data
            }
            return Response(response_data, status=HTTP_200_OK)

        return Response({'detail': 'Unauthorized'}, status=HTTP_403_FORBIDDEN)
    def create(self, request, *args, **kwargs):
            # Verificar si el usuario es un Moneylender
            if not hasattr(request.user, 'moneylender'):
                raise PermissionDenied("No tienes permiso para crear un préstamo.")

            # Obtener el Moneylender asociado al usuario
            moneylender = request.user.moneylender

            # Verificar si is_subscribed es True
            if not moneylender.is_subscribed:
                raise PermissionDenied("El Moneylender no está suscrito.")

            # Usar el serializer para validar los datos del préstamo
            moneylender_loan_serializer = MoneylenderLoanSerializer(data=request.data)
            if moneylender_loan_serializer.is_valid():
                # Obtener los datos validados
                validated_data = moneylender_loan_serializer.validated_data
                
                # Extraer los datos necesarios
                loan_amount = validated_data['amount']
                interest_rate = validated_data['interest_rate'] / 100  
                number_of_payments = validated_data['number_of_payments']
                term = validated_data['term']

                # Calcular el total a pagar
                total_amount =  loan_amount  + (loan_amount * interest_rate)
                # Calcular el pago por término
                payment_per_term = total_amount / number_of_payments
                # Crear el préstamo
                loan = Loan.objects.create(
                    moneylender=moneylender,
                    amount=loan_amount,
                    interest_rate=validated_data['interest_rate'],
                    number_of_payments=number_of_payments,
                    term=term,
                    total_amount=total_amount,
                    payment_per_term=payment_per_term,
                    difficulty=12,  # Valor predeterminado
                    duration_loan="Duración predeterminada",  # Valor predeterminado
                    publication_date=timezone.now()
                     
                )
                
                loan.difficulty = calcular_dificultad(loan)
                loan.save()
                
                return Response(moneylender_loan_serializer.data, status=HTTP_201_CREATED)

            return Response(moneylender_loan_serializer.errors, status=HTTP_400_BAD_REQUEST)  

#Vista de modelo para money lender
class MoneylenderViewSet(viewsets.ModelViewSet):
    
    queryset = Moneylender.objects.all()

    def get_serializer_class(self):
        # Seleccionar el serializer adecuado basado en el tipo de cuenta del usuario
        if hasattr(self.request.user, 'moneylender'):
            return MoneylenderDetailSerializer
        elif hasattr(self.request.user, 'borrower'):
            return MoneylenderSerializer
        else:
            return MoneylenderSerializer  # Usa el serializer general en otros casos

    def list(self, request):
        instance = get_object_or_404(Moneylender, user_id=request.user.id)
        serializer = self.get_serializer(instance)
        return Response({"stats": serializer.data})

#Vista de modelo para credit history
class CreditHistoryViewSet(viewsets.ModelViewSet):
    queryset = CreditHistory.objects.all()
    serializer_class = CreditHistorySerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer

#Vista de modelo para ver usuarios registrados
User = get_user_model()
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_serializer_class(self):
    # Seleccionar el serializer adecuado basado en el tipo de cuenta
        if hasattr(self.request.user, 'moneylender'):
            return MoneylenderSerializer  # Serializer para Moneylender
        elif hasattr(self.request.user, 'borrower'):
            return BorrowerSerializer  
        else:
            return UserSerializer
        
    def retrieve(self, request, *args, **kwargs):
        # Obtener el usuario autenticado
        user = request.user
    
        try:
   
            if hasattr(user, 'moneylender'):
                person = Moneylender.objects.get(user=user)  
                serializer = MoneylenderSerializer(person)  
            elif hasattr(user, 'borrower'):
                person = Borrower.objects.get(user=user) 
                serializer = BorrowerSerializer(person)  
            else:
                return Response({"detail": "Person not found."}, status=HTTP_404_NOT_FOUND)

            return Response(serializer.data, status=HTTP_200_OK)

        except (Moneylender.DoesNotExist, Borrower.DoesNotExist):
            return Response({"detail": "Person not found."}, status=HTTP_404_NOT_FOUND)
        
        
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
            return Request.objects.all()  # No hay solicitudes para este usuario

    def get_serializer_class(self):
        # Seleccionar el serializer adecuado basado en el tipo de cuenta
        if hasattr(self.request.user, 'moneylender'):
            return MoneylenderRequestsSerializer
        elif hasattr(self.request.user, 'borrower'):
            return BorrowerRequestSerializer
        else:
            return RequestSerializer  # Usa el serializer por defecto
        
    def create(self, request, *args, **kwargs):
        serializer = BorrowerRequestSerializer(data=request.data)

        if serializer.is_valid():
            moneylender_id = serializer.validated_data['moneylender_id']
            loan_id = serializer.validated_data['loan_id']

            try:
                moneylender = Moneylender.objects.get(id=moneylender_id)
                loan = Loan.objects.get(id=loan_id)
            except (Moneylender.DoesNotExist, Loan.DoesNotExist):
                return Response({"error": "Moneylender or Loan not found."}, status=HTTP_404_NOT_FOUND)

            # Crear la instancia de Request
            request_instance = Request.objects.create(
                borrower=request.user.borrower,
                moneylender=moneylender,
                loan=loan,
                status='pending'
            )

            response_serializer = BorrowerRequestSerializer(request_instance)
            return Response(response_serializer.data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    def get_serializer_class(self):
    # Seleccionar el serializer adecuado basado en el tipo de cuenta
        if hasattr(self.request.user, 'moneylender'):
            return MoneylenderTransactionSerializer  # Serializer para Moneylender
        elif hasattr(self.request.user, 'borrower'):
            return TransactionSerializer  
        else:
            return TransactionSerializer 
        
    def list(self, request):
        # Verificar si el usuario es un Moneylender
        if hasattr(request.user, 'moneylender'):
            moneylender = request.user.moneylender  
            
            # Obtener todos los ActiveLoans asociados al Moneylender
            active_loans = ActiveLoan.objects.filter(moneylender=moneylender)
            
            # Obtener todas las transacciones asociadas a estos ActiveLoans
            transactions = Transaction.objects.filter(active_loan__in=active_loans)
            transactions = transactions.order_by('-payment_date')
            
            # Serializar los datos del Moneylender y sus transacciones
            serializer = MoneylenderTransactionSerializer(moneylender)
            
            return Response(serializer.data['transactions'], status=HTTP_200_OK)
        
        # Si el usuario no es un Moneylender, se asume que es un Borrower
        elif hasattr(request.user, 'borrower'):
            borrower = request.user.borrower  # Obtener el objeto Borrower del usuario autenticado

            # Obtener todos los ActiveLoans asociados al Borrower
            active_loans = ActiveLoan.objects.filter(borrower=borrower)

            # Obtener todas las transacciones asociadas a estos ActiveLoans
            transactions = Transaction.objects.filter(active_loan__in=active_loans).order_by('-payment_date')

            # Serializar las transacciones asociadas al Borrower
            serializer = TransactionSerializer(transactions, many=True)

            return Response(serializer.data, status=HTTP_200_OK)

        # Si el usuario no es un Moneylender, retornar error
        return Response({"detail": "No se puede determinar el rol del usuario."}, status=HTTP_400_BAD_REQUEST)

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
        ('active_loan', ActiveLoanViewSet),
        ('payment', PaymentViewSet)
    ]
    routers = {}
    for basename, viewset in viewsets_with_basenames:
        router = DefaultRouter()
        router.register(r'', viewset, basename=basename)
        routers[basename] = router
        
    return routers