from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from database.models import Borrower
from database.serializers import BorrowerSerializer
import os

#Puse como defecto el token que habias puesto en caso de que no crees el .env aun
TOKEN_MOFFIN = os.getenv('ACCESS_TOKEN_MOFFIN', 'd0a8721978878bd705228203826fa9178a1f2c496db20e4402f92ff84b2b3379')
class ReporteBdC(APIView):
    #Agreguee el serializer_class para hacer pruebas en swagger
    serializer_class = BorrowerSerializer
    def post(self, request, *args, **kwargs):
        borrower = Borrower.objects.all()
        serializer = BorrowerSerializer(borrower, many=True)

        # Configurar la URL de la API y obtener el token de la variable de entorno
        api_url = "https://staging.moffin.mx/api/v1/query/bureau_pf"
        
        headers = {
            'Authorization': f'Bearer {TOKEN_MOFFIN}',  
            'Content-Type': 'application/json'  
        }

        data = {
            'birthdate': request.data.get('birt_date', None),
            'firstName': request.data.get('firsn_name', None),
            'middleName': request.data.get('midle_Name', None),
            'firstLastName': request.data.get('first_surname', None),
            'secondLastName': request.data.get('second_surname', None),
            'accountType' : request.data.get('accountType', None),
            'rfc': request.data.get('rfc', None),
            'address': request.data.get('full_address', None),
            'municipality': request.data.get('municipality', None),
            'neighborhood': request.data.get('neighborhood', None),
            'zipCode': request.data.get('postal_code', None),
            'state': request.data.get('state', None),
            'city': request.data.get('city', None),
            'country': request.data.get('country', None),
            'exteriorNumber': request.data.get('exteriorNumber', None),
            'nationality': request.data.get('nationality', None)
        }
        
        try:
            # Hacer una solicitud POST a la API externa con el token y los datos en JSON
            api_response = requests.post(api_url, json=data, headers=headers)
            api_response.raise_for_status()  # Verifica si la solicitud fue exitosa
            api_data = api_response.json()

            # Combinar los datos de la base de datos con los datos de la API externa
            combined_data = {
                'borrower': serializer.data,  # Datos de la base de datos
                'api_data': api_data           # Datos de la API externa
            }

            return Response(combined_data, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)