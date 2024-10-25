import os
import requests
from rest_framework.views import APIView
from rest_framework import status
from services.Moffin.validation import UploadScore
from database.models import Borrower
from rest_framework.response import Response
from database.serializers import BorrowerSerializer
import environ

# Inicializa el entorno de variables
env = environ.Env()
environ.Env.read_env()  # Lee el archivo .env

# Obtén el token
api_token = env("ACCES_TOKEN_MOFFIN") 





class ObtenerSat(APIView):
    def post(self, request, *args, **kwargs):
        borrower = Borrower.objects.all()
        serializer = BorrowerSerializer(borrower, many=True)
        url="https://staging.moffin.mx/api/v1/query/bureau_pf"
        token= api_token

        headers = {
            'Authorization': f'Bearer {token}',  
            'Content-Type': 'application/json'  
        }
