from rest_framework import serializers
"""
Es el serializer que espera los datos del usuario para despues ser llamados por el api de moffin

        Parámetros:
            birthdate:
                Descripción: Fecha de nacimiento de la persona. Obligatorio
            firstName:
                Descripción: Primer nombre de la persona. Obligatorio
            firstLastName:
                Descripción: Primer apellido de la persona. Obligatorio
            rfc:
                Descripción: Registro Federal de Contribuyentes (RFC) de la persona. Obligatorio
            address:
                Descripción: Dirección completa. Obligatorio
            city:
                Descripción: Ciudad de residencia. Obligatorio
            municipality:
                Descripción: Municipio de residencia. Obligatorio
            state:
                Descripción: Estado de residencia. Obligatorio
            zipCode:
                Descripción: Código postal. Obligatorio
            neighborhood:
                Descripción: Colonia o vecindario. Obligatorio
            country:
                Descripción: País de residencia. Obligatorio
            nationality:
                Descripción: Nacionalidad de la persona. Obligatorio
        Proceso:
            - Recibe los datos del diccionario JSON 
"""
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