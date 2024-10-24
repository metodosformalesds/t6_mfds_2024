from rest_framework import serializers
from django.contrib.auth.models import User
from database.models import Moneylender, Borrower
from database.serializers import MoneylenderSerializer, BorrowerSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['id', 'username', 'email', 'password']

class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    account_type = serializers.ChoiceField(choices=[('borrower', 'Borrower'), ('moneylender', 'Moneylender')])