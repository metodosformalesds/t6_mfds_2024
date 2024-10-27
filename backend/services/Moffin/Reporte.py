from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from database.models import Borrower
import requests
import os

TOKEN_MOFFIN = os.getenv('ACCESS_TOKEN_MOFFIN', 'Token d0a8721978878bd705228203826fa9178a1f2c496db20e4402f92ff84b2b3379')

class ReporteSerializer(serializers.Serializer):
    user = serializers.IntegerField(required=True)  

class Reporte(APIView):
    serializer_class = ReporteSerializer
    
    def post(self, request):
        serializer = ReporteSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            
            try:
                borrower = Borrower.objects.get(id=user)
            except Borrower.DoesNotExist:
                return Response({'error': 'Borrower not found.'}, status=status.HTTP_404_NOT_FOUND)
            
            # Datos específicos del prestatario para la API externa
            data = {    
                'birthdate': borrower.birth_date.strftime('%Y-%m-%d'),
                'firstName': borrower.first_name,
                'firstLastName': borrower.first_name,
                'secondLastName': borrower.second_surname,
                'rfc': borrower.rfc,
                'accountType': "PF",
                'address': borrower.full_address,
                'city': borrower.city,
                'municipality': borrower.municipality,
                'state': borrower.state,
                'zipCode': borrower.postal_code,
                'neighborhood': borrower.neighborhood,
                'country': borrower.country,
                'nationality': borrower.nationality
            }

            # Configurar la solicitud a la API externa
            api_url = "https://sandbox.moffin.mx/api/v1/query/bureau_pf"
            headers = {
                'Authorization': 'Token d0a8721978878bd705228203826fa9178a1f2c496db20e4402f92ff84b2b3379',
                'Content-Type': 'application/json'
            }

            try:
                # Hacer la solicitud POST a la API externa
                api_response = requests.post(api_url, json=data, headers=headers)
                api_response.raise_for_status()
                api_data = api_response.json()

                return Response({'api_data': api_data}, status=status.HTTP_200_OK)

            except requests.exceptions.RequestException as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)