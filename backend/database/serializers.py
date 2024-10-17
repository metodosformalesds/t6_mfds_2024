from rest_framework import serializers
from .models import CreditHistory, Moneylender, Loans, Borrower, ActiveLoans, InvoiceHistory, UserRequest, Transaction



#Serializer del historial crediticio
class CreditHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditHistory
        fields = '__all__'  # Esto incluye todos los campos del modelo

#serializer del prestamista
class MoneylenderSerializer(serializers.ModelSerializer):
    class meta:
        model = Moneylender
        fields = '__all__'

#Serializer de los prestamos
class LoansSerializer(serializers.ModelSerializer):
    class meta:
        model = Loans
        fields = '__all__'

#Serializer del prestatario
class BorrowerSerializer(serializers.ModelSerializer):
    class meta:
        model = Borrower
        fields = '__all__'

#Serializer de los detalles de los prestamos
class ActiveLoansSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveLoans
        fields = '__all__'
        
#Serializer del historial de facturas
class InvoiceHistorySerializer(serializers.ModelSerializer):
    class meta:
        model = InvoiceHistory
        fields = '__all__'

#Serializer de las solicitudes de prestamo
class UserRequestSerializer(serializers.ModelSerializer):
    class meta:
        model = UserRequest
        fields = '__all__'

#Serializer de los detalles de los prestamos
class ActiveLoansSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveLoans
        fields = '__all__'
        
#Serializer de las solicitudes transaccionadas
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction  # Asegúrate de que este modelo exista y sea correcto
        fields = '__all__'
        
class PaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3)

class PayoutSerializer(serializers.Serializer):
    recipient_email = serializers.EmailField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3, default='USD')
    

