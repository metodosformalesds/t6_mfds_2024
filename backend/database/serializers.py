from rest_framework import serializers
from .models import CreditHistory, Moneylender, Loan, Borrower, ActiveLoan, InvoiceHistory, Request, Transaction
from django.contrib.auth.models import User

#Serializer del historial crediticio
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
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    credit_history = CreditHistorySerializer(many=True, read_only=True) 

    class Meta:
        model = Borrower
        fields = [
            'id', 'first_name', 'middle_name', 'first_surname', 'second_surname', 'birth_date',
            'phone_number', 'rfc', 'ciec', 'full_address', 'city', 'neighborhood', 'postal_code', 
            'state', 'country', 'municipality', 'nationality', 'possibility_of_pay', 
            'score_llamas', 'credit_history', 'user'
        ]
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


#Serializer de los detalles de los prestamos
class ActiveLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveLoan
        fields = '__all__'
        
#Serializer de las solicitudes transaccionadas
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction 
        fields = '__all__'



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