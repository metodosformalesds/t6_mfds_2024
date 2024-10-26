import os
import requests
from rest_framework.views import APIView
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
#Monto= Monto a pagar
#Porcentaje_Prestamo=Porcentaje del prestamo
#Descuento_MalP= Porcentaje de Descuento por no pagar a tiempo
#N_CuotasS= Numero de cuotas sin pagar
#Pagos_Fuera_Fecha= Pagos realizado despues de el plazo establecido para realizarlo
#Total= Puntos totales
#valor_obtenido= valor obtenido de puntos



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class MiVista(APIView):
    def post(self, request, *args, **kwargs):
        Monto = request.data.get("Monto")
        N_CuotasS = request.data.get("N_CuotasS")
        Pagos_Fuera_Fecha = request.data.get("Pagos_Fuera_Fecha")
        Total = request.data.get("Total")
        
        # Validar que todos los valores estén presentes
        if Monto is None or N_CuotasS is None or Pagos_Fuera_Fecha is None or Total is None:
            return Response({"error": "Valores no proporcionados"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Intentar convertir Monto a float
        try:
            Monto = float(Monto)
        except ValueError:
            return Response({"error": "Valores deben ser numéricos"}, status=status.HTTP_400_BAD_REQUEST)
        
  