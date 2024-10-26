import os
import requests
from rest_framework.views import APIView
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from services.Score.serializer import ScoreSerializer
#Monto= Monto a pagar
#Porcentaje_Prestamo=Porcentaje del prestamo
#Descuento_MalP= Porcentaje de Descuento por no pagar a tiempo
#N_CuotasS= Numero de cuotas sin pagar
#Pagos_Fuera_Fecha= Pagos realizado despues de el plazo establecido para realizarlo
#Total= Puntos totales
#valor_obtenido= valor obtenido de puntos

# Funciones para aumentar y reducir el score
porcentaje_Prestamo = 0.06
Descuento_MalP = 0.1

def aumentar_Score(monto, n_cuotas, pagos_fuera_fecha, total):
    valor_obtenido = n_cuotas * (monto * porcentaje_Prestamo)
    return total + valor_obtenido

def reducir_Score(monto, n_cuotas, pagos_fuera_fecha, total):
    valor_obtenido = -(pagos_fuera_fecha * (monto * Descuento_MalP))
    return total + valor_obtenido

# Vista con el serializer incorporado
class ObtenerScore(APIView):
    serializer_class=ScoreSerializer
    def post(self, request, *args, **kwargs):
        # Validar datos con el serializer
        serializer = ScoreSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extraer y convertir los datos
        try:
            monto = float(serializer.validated_data["Monto"])
            n_cuotas = float(serializer.validated_data["N_CuotasS"])
            pagos_fuera_fecha = float(serializer.validated_data["Pagos_Fuera_Fecha"])
            total = float(serializer.validated_data["Total"])
            operacion = serializer.validated_data["Operacion"]
        except (TypeError, ValueError):
            return Response({"error": "Valores deben ser numéricos"}, status=status.HTTP_400_BAD_REQUEST)

        # Selección de la operación
        operaciones = {
            'aumentar_Score': aumentar_Score,
            'reducir_Score': reducir_Score
        }
        funcion_operacion = operaciones.get(operacion)
        if funcion_operacion is None:
            return Response({"error": "Operación no válida"}, status=status.HTTP_400_BAD_REQUEST)

        # Calcular y devolver el resultado
        resultado = funcion_operacion(monto, n_cuotas, pagos_fuera_fecha, total)
        return Response({"resultado": resultado}, status=status.HTTP_200_OK)