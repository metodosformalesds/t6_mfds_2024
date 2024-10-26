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

#Serializer del prestatario
class BorrowerSerializer(serializers.ModelSerializer):
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

#Serializer de las solicitudes de prestamo
class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'

#Serializer de los detalles de los prestamos
class ActiveLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveLoan
        fields = '__all__'
        
#Serializer de las solicitudes transaccionadas
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction  # Asegúrate de que este modelo exista y sea correcto
        fields = '__all__'

class BdCSerializer(serializers.ModelSerializer):
    birthdate = serializers.DateField(source='birth_date')
    firstName = serializers.CharField(source='first_name')
    firstLastName = serializers.CharField(source='first_surname')
    secondLastName = serializers.CharField(source='second_surname')
    rfc = serializers.CharField()
    accountType = serializers.CharField(default='PF')
    address = serializers.CharField(source='full_address')
    city = serializers.CharField()
    municipality = serializers.CharField()
    state = serializers.CharField()
    zipCode = serializers.CharField(source='postal_code')
    neighborhood = serializers.CharField()
    country = serializers.CharField()

    class Meta:
        model = Borrower
        fields = [
            'birthdate', 'firstName', 'firstLastName', 'secondLastName', 
            'rfc', 'accountType', 'address', 'city', 'municipality', 
            'state', 'zipCode', 'neighborhood', 'country'
        ]
