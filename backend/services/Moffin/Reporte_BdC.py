from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from database.models import Borrower, CreditHistory
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
                
                score_data = api_data.get('response', {}).get('return', {}).get('Personas', {}).get('Persona', [])[0].get('ScoreBuroCredito', {}).get('ScoreBC', [{}])[0]
                ##resumen_data = api_data.get('response', {}).get('return', {}).get('Personas', {}).get('Persona', [{}])[0].get('ResumenReporte', [{}])[0]
                ##empleos_data = api_data.get("response", {}).get("return", {}).get("Personas", {}).get("Persona", [])[0].get("Empleos", {}).get("Empleo", [])
                
                credit_history = CreditHistory(
                    borrower=borrower,
                    #accounts_open=int(resumen_data.get('NumeroCuentas', 0)),
                    #accounts_closed=int(resumen_data.get('CuentasCerradas', 0)),
                    #num_mop1=int(resumen_data.get('NumeroMOP1', 0)),
                    #num_mop2=int(resumen_data.get('NumeroMOP2', 0)),
                    #num_mop3=int(resumen_data.get('NumeroMOP3', 0)),
                    #num_mop4=int(resumen_data.get('NumeroMOP4', 0)),
                    #num_mop5=int(resumen_data.get('NumeroMOP5', 0)),
                    #num_mop6=int(resumen_data.get('NumeroMOP6', 0)),
                    #num_mop7=int(resumen_data.get('NumeroMOP7', 0)),
                    code_score=(score_data.get('CodigoScore', 0)), 
                    val_score=(score_data.get('Valorscore', 0)), 
                    #place_of_work=(empleos_data.get('NombreEmpresa', 0)),
                    #salary=float(empleos_data.get('Salario', 0)),
                )
                
                credit_history.save()
                
                return Response({'api_data': api_data}, status=status.HTTP_200_OK)

            except requests.exceptions.RequestException as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
