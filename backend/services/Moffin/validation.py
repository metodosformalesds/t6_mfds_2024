from rest_framework import serializers

# Serializer para manejar la consulta del SAT:
class UploadScore(serializers.Serializer):
    externalID= serializers.CharField(required=True, max_length=100)  # Campo para el Id
    rfc=serializers.CharField(required=True, max_length=255)  # Campo para el rfc
    CIEC=serializers.CharField(required=True, max_length=255)  # Campo para el CIEC 
    startdate=serializers.DateField() #Campo de fecha de inicio.
    enddat=serializers.DateField() #Campo de fecha de finalización.