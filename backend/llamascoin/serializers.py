from rest_framework import serializers
#from django.contrib.auth.models import User
from database.models import Moneylender, Borrower, User
from database.serializers import MoneylenderSerializer, BorrowerSerializer
#Serializer para crear cuenta de usuario provisional
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','paypal_email','password','curp', 'account_type']
        extra_akwargs = {
            'password': {'write_only': True}
        }