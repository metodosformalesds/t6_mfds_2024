from rest_framework import serializers
from .models import CreditHistory, Moneylender, Loans, Borrower, LoanDetails, InvoiceHistory, UserRequest



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
class LoanDetailsSerializer(serializers.ModelSerializer):
    class meta:
        model = LoanDetails
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