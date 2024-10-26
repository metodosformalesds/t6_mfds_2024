from rest_framework import serializers
from database.models import Borrower

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