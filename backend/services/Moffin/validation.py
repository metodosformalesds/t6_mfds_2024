from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
import cv2
import easyocr
import re
import numpy as np
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

# Serializer para manejar la consulta del SAT:
class UploadScore(serializers.Serializer):
    externalID= serializers.CharField(required=True, max_length=100)  # Campo para el Id
    rfc=serializers.CharField(required=True, max_length=255)  # Campo para el rfc
    CIEC=serializers.CharField(required=True, max_length=255)  # Campo para el CIEC 
    startdate=serializers.DateField() #Campo de fecha de inicio.
    enddat=serializers.DateField() #Campo de fecha de finalización.