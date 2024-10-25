import os
import requests
from rest_framework.views import APIView
from rest_framework import status
from services.Moffin.validation import UploadScore
from database.models import Borrower
from rest_framework.response import Response
from database.serializers import BorrowerSerializer
import os

# Obtén el token
api_token = os.getenv("ACCESS_TOKEN_MOFFIN") 

class ObtenerSat(APIView):
    def post(self, request, *args, **kwargs):
        borrower = Borrower.objects.all()
        serializer = BorrowerSerializer(borrower, many=True)
        url="https://sandbox.moffin.mx/api/v1/query/prospector_pf"
        token= api_token

        headers = {
            'Authorization': f'Bearer {token}',  
            'Content-Type': 'application/json'  
        }
        birthdate=request.data.get('birthdate', None)
        email=request.data.get('email', None)
        firstName=request.data.get('firstName', None)
        firstLastName=request.data.get('firstLastName', None)
        secondLastName=request.data.get('secondLastName', None)
        rfc=request.data.get('rfc', None)
        accountType=request.data.get('accountType', None)
        address=request.data.get('address', None)
        city=request.data.get('city', None)
        municipality=request.data.get('municipality', None)
        state=request.data.get('state', None)
        zipCode=request.data.get('zipCode', None)
        exteriorNumber=request.data.get('exteriorNumber', None)
        neighborhood=request.data.get('neighborhood', None)
        country=request.data.get('country', None)
        nationality=request.data.get('nationality', None)
        data = {
           'birthdate':birthdate,
           'email':email,
           'firstName':firstName,
           'firstLastName':firstLastName,
           'secondLastName':secondLastName,
           'rfc':rfc,
           'accountType':accountType,
           'address':address,
           'city':city,
           'municipality':municipality,
           'state':state,
           'zipCode':zipCode,
           'exteriorNumber':exteriorNumber,
           'neighborhood':neighborhood,
           'country':country,
           'nationality':nationality
        }
        try:
            api_response = requests.post(url, json=data, headers=headers)
            api_response.raise_for_status()
            api_data = api_response.json()

            # Devolver la respuesta de la API externa como respuesta en la vista
            return Response(api_data, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            # Manejar errores de solicitud
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
