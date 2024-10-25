import os
import requests
from rest_framework.views import APIView
from rest_framework import status
from services.Moffin.validation import UploadScore
from database.models import Borrower
from rest_framework.response import Response

def analizar_datos(datos):
    # Definir la URL del endpoint de la API de Moffin
    url ='https://sandbox.moffin.mx/api/v1/query/bureau_pf'
    SECRET_MOFFIN = os.getenv('ACCES_TOKEN_MOFFIN', '')
    
    # Configurar los headers para la autenticación
    headers = {
        'Authorization': f'Bearer {SECRET_MOFFIN}',
        'Content-Type': 'application/json',
    }
    
    # Enviar una solicitud POST a la API de Moffin con los datos a analizar
    try:
        response = requests.post(url, json=datos, headers=headers)
        response.raise_for_status()  # Lanza una excepción si la respuesta tiene un error de HTTP
        return response.json()  # Retorna la respuesta en formato JSON
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Manejar errores HTTP
        return None