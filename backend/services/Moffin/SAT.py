import os
import requests
from rest_framework.views import APIView
from rest_framework import status
from services.Moffin.validation import UploadScore
from database.models import Borrower
from rest_framework.response import Response

CLIENT_ID_MOFFIN = os.getenv('CLIENT_ID_SAT', 'Default_Secret')
SECRET_MOFFIN = os.getenv('SECRET_MOFFIN', '')
def get_moffin_access_token():
    client_id = CLIENT_ID_MOFFIN
    secret = SECRET_MOFFIN
    url = "https://sandbox.moffin.mx/api/v1"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US"
    }
    response = requests.post(url, headers=headers, auth=(client_id, secret), data={"grant_type": "client_credentials"})
    return response.json().get("access_token")

class CreateObtenerSAT(APIView):
    serializer_class = UploadScore
    def post(self, request):
        serializer = UploadScore(data=request.data)
        if serializer.is_valid():
            access_token_moffin = get_moffin_access_token()
            url = ""
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token_moffin}"
            }
        