from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import  CreditHistory, Moneylender, Loan, Borrower, ActiveLoan, InvoiceHistory, Payments, Request, Transaction
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()
INTEREST_BANK = float(os.getenv('INTEREST_BANK', 28.18))
##from django.contrib.auth.models import User
#Serializer del historial crediticio
User = get_user_model()
class CreditHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditHistory
        fields = '__all__'  # Esto incluye todos los campos del modelo

#serializer del prestamista
class MoneylenderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    class Meta:
        model = Moneylender
        fields = '__all__'

#Serializer de los prestamos
class LoansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
#Serializer de las solicitudes de prestamo
class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'
        
#Serializer del prestatario
class BorrowerSerializer(serializers.ModelSerializer):
    credit_history = CreditHistorySerializer(many=True, read_only=True) 
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = Borrower
        fields = '__all__'

#Serializer de los detalles de los prestamos
class ActiveLoansSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveLoan
        fields = '__all__'
        
#Serializer del historial de facturas
class InvoiceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceHistory
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'
#Serializer de los detalles de los prestamos
class ActiveLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveLoan
        fields = '__all__'
        
#Serializer de las solicitudes transaccionadas
class TransactionSerializer(serializers.ModelSerializer):
    # Sobrescribir 'payment_date' para mostrar solo la fecha
    payment_date = serializers.SerializerMethodField()
    class Meta:
        model = Transaction
        fields = '__all__'

    def get_payment_date(self, obj):
        return obj.payment_date.date()  # Esto devuelve solo la fecha (sin hora)


class BorrowerMoneylenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moneylender
        fields = ['id', 'first_name','middle_name', 'first_surname', 'second_surname', 'birth_date', 'phone_number', 'rfc'] 

class BorrowerLoanSerializer(serializers.ModelSerializer):
    request_status = serializers.SerializerMethodField()  
    moneylender= BorrowerMoneylenderSerializer(read_only=True) 
    
    class Meta:
        model = Loan
        fields = [
            'id',
            'moneylender',
            'amount',
            'total_amount',
            'difficulty',
            'interest_rate',
            'number_of_payments',
            'term',
            'publication_date',
            'payment_per_term',
            'moneylender',
            'request_status'
        ]
        
    def get_request_status(self, obj):
        borrower_id = self.context.get('borrower_id')  

        # Filtrar las solicitudes del Borrower para cada préstamo 
        request = Request.objects.filter(loan=obj, borrower_id=borrower_id).first()

        if request:
            return request.status  # Retorna el estado si existe
        return ''  
    

class MoneylenderBorrowerSerializer(serializers.ModelSerializer):
    credit_history = CreditHistorySerializer(many=True, read_only=True) 
    class Meta:
        model = Borrower
        fields = ['id', 'first_name', 'middle_name', 'first_surname', 'second_surname', 'birth_date', 'rfc', 'credit_history']
    
class MoneylenderRequestsSerializer(serializers.ModelSerializer):
    borrower = MoneylenderBorrowerSerializer(read_only=True)
    loan = LoansSerializer(read_only=True) 

    class Meta:
        model = Request
        fields = ['id', 'borrower', 'loan', 'status', 'created_at']  
        
class MoneylenderLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['amount', 'interest_rate', 'number_of_payments', 'term']

    # Validar la tasa de interés
    def validate_interest_rate(self, value):
        if value > INTEREST_BANK:
            raise serializers.ValidationError(f"La tasa de interés no puede exceder el {INTEREST_BANK}%")
        return value

    # Validar el monto del préstamo
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("El monto del préstamo debe ser mayor que 0")
        return value

    # Validar el número de pagos
    def validate_number_of_payments(self, value):
        if value <= 0:
            raise serializers.ValidationError("El número de pagos debe ser mayor que 0")
        return value

    # Validación de varios campos
    def validate(self, data):
        # Ejemplo: Validar que el número de pagos y el término sean consistentes
        if data['term'] == 1 and data['number_of_payments'] > 52:  # Semanalmente, máximo 52 semanas
            raise serializers.ValidationError("Número de pagos no puede exceder las 52 semanas en plazo semanal")
        if data['term'] == 2 and data['number_of_payments'] > 24:  # Quincenalmente, máximo 24 quincenas
            raise serializers.ValidationError("Número de pagos no puede exceder las 24 quincenas en plazo quincenal")
        if data['term'] == 3 and data['number_of_payments'] > 12:  # Mensual, máximo 12 meses
            raise serializers.ValidationError("Número de pagos no puede exceder los 12 meses en plazo mensual")

        return data
class BorrowerCreditHistorySerializer(serializers.ModelSerializer):
    credit_history = CreditHistorySerializer(many=True, read_only=True)  
    class Meta:
        model = Borrower
        fields = [
            'first_name', 'middle_name', 'first_surname', 'second_surname', 'credit_history', 'rfc'
        ]

class BorrowerRequestSerializer(serializers.ModelSerializer):
    moneylender_id = serializers.IntegerField()
    loan_id = serializers.IntegerField()
    class Meta:
        model = Request
        fields = ['moneylender_id', 'loan_id']
        
        
class BorrowerActiveLoanSerializer(serializers.ModelSerializer):
    moneylender = BorrowerMoneylenderSerializer(read_only=True)  # Serializer for related Moneylender
    loan = LoansSerializer(read_only=True)  # Serializer for related Loan
    payments = PaymentSerializer(many=True, read_only=True)
    
    class Meta:
        model = ActiveLoan
        fields = [
            'id',
             #Campos de ActiveLoan
            'total_debt_paid',
            'amount_to_pay',
            'start_date',
            'loan',
            'moneylender',
            'payments',
        ]
class MoneylenderTransactionSerializer(serializers.ModelSerializer):
    transactions = serializers.SerializerMethodField()
    
    class Meta:
        model = Moneylender
        fields = ['transactions']

    def get_transactions(self, obj):
        # Obtener las transacciones asociadas al Moneylender
        active_loans = ActiveLoan.objects.filter(moneylender=obj)
        transactions = Transaction.objects.filter(active_loan__in=active_loans)

        # Serializar cada transacción
        transaction_data = []
        for transaction in transactions:
            # Determinar la persona asociada a la transacción
            if transaction.transaction_type == 'payout':
                person_data = {
                    'id': transaction.active_loan.moneylender.id,
                    'first_name': transaction.active_loan.moneylender.first_name,
                    'middle_name': transaction.active_loan.moneylender.middle_name,
                    'first_surname': transaction.active_loan.moneylender.first_surname,
                    'second_surname': transaction.active_loan.moneylender.second_surname,
                    'rfc': transaction.active_loan.moneylender.rfc,
                }
            elif transaction.transaction_type == 'payment':
                person_data = {
                    'id': transaction.active_loan.borrower.id,
                    'first_name': transaction.active_loan.borrower.first_name,
                    'middle_name': transaction.active_loan.borrower.middle_name,
                    'first_surname': transaction.active_loan.borrower.first_surname,
                    'second_surname': transaction.active_loan.borrower.second_surname,
                    'rfc': transaction.active_loan.borrower.rfc,
                }
            else:
                person_data = {}

            transaction_data.append({
                'id': transaction.id,
                'amount_paid': transaction.amount_paid,
                'payment_date': transaction.payment_date,
                'transaction_type': transaction.transaction_type,
                'status': transaction.status,
                'paypal_transaction_id': transaction.paypal_transaction_id,
                'person': person_data  
            })

        return transaction_data