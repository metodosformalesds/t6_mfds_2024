from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from database.models import CreditHistory
from database.serializers import CreditHistorySerializer
# Create your views here.

#Vista super simple para probar el frontend
class HelloWorld(APIView):
    def get(self, request):
        return Response({'message': '¡Hola desde el backend!'}, status=200)


#Vista de modelo para credit history
class CreditHistoryViewSet(viewsets.ModelViewSet):
    queryset = CreditHistory.objects.all()
    serializer_class = CreditHistorySerializer

    def list(self, request, *args, **kwargs):
        return Response({'message': '¡Hola desde el backend!'})