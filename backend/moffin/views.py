from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from database.models import Borrower
from database.serializers import BorrowerSerializer
import environ

env = environ.Env()
environ.Env.read_env()  

class Muffin(APIView):
    def post(self, request, *args, **kwargs):
        borrower = Borrower.objects.all()
        serializer = BorrowerSerializer(borrower, many=True)

        # Configurar la URL de la API y obtener el token de la variable de entorno
        api_url = "https://staging.moffin.mx/api/v1/query/bureau_pf"
        token = env('d0a8721978878bd705228203826fa9178a1f2c496db20e4402f92ff84b2b3379')

        headers = {
            'Authorization': f'Bearer {token}',  
            'Content-Type': 'application/json'  
        }

        data = {
            'birthdate': request.data.get('birthdate', None),
            'FirstName': request.data.get('FirstName', None),
            'firstLastName': request.data.get('firstLastName', None),
            'secondLastName': request.data.get('secondLastName', None),
            'rfc': request.data.get('rfc', None),
            'address': request.data.get('address', None),
            'neighborhood': request.data.get('neighborhood', None),
            'city': request.data.get('city', None),
            'municipality': request.data.get('municipality', None),
            'state': request.data.get('state', None),
            'zipCode': request.data.get('zipCode', None),
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
        

