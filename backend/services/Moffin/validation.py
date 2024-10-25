from rest_framework import serializers

# Serializer para manejar la consulta del score:
class UploadScore(serializers.Serializer):
    birthdate= serializers.CharField(required=True) 
    firstName= serializers.CharField(required=True, max_length=255)  
    firstLastName= serializers.CharField(required=True, max_length=255)  
    rfc= serializers.CharField(required=True, max_length=255)  
    address= serializers.CharField(required=True, max_length=255)  
    city= serializers.CharField(required=True, max_length=255)  
    municipality= serializers.CharField(required=True, max_length=255)  
    state= serializers.CharField(required=True, max_length=255)  
    zipCode= serializers.CharField(required=True, max_length=255)  
    neighborhood= serializers.CharField(required=True, max_length=255)  
    country= serializers.CharField(required=True, max_length=255)  
    nationality= serializers.CharField(required=True, max_length=255)  