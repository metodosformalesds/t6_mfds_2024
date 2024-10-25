import os
import requests
from rest_framework.views import APIView
from rest_framework import status
from services.Moffin.validation import UploadScore
from database.models import Borrower
from rest_framework.response import Response

# Obtén el token
api_token = os.getenv("ACCESS_TOKEN_MOFFIN")

class ObtenerSat(APIView):
    serializer_class=UploadScore

    def post(self, request, *args, **kwargs):
        # Instanciar el serializer con los datos de la solicitud
        serializer = UploadScore(data=request.data)
        # Verificar si los datos son válidos
        if serializer.is_valid():
            # Obtener los datos validados
            data = serializer.validated_data
            
            # Preparar la solicitud a la API externa
            url = "https://sandbox.moffin.mx/api/v1/query/prospector_pf"
            headers = {
                'Authorization': f'Bearer {api_token}',  
                'Content-Type': 'application/json'  
            }

            try:
                # Realizar la solicitud POST a la API externa
                api_response = requests.post(url, json=data, headers=headers)
                api_response.raise_for_status()  # Lanza un error si la respuesta fue un error HTTP

                # Devolver la respuesta de la API externa como respuesta en la vista
                return Response(api_response.json(), status=status.HTTP_200_OK)

            except requests.exceptions.RequestException as e:
                # Manejar errores de solicitud
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        # Si los datos no son válidos, devolver los errores de validación
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
