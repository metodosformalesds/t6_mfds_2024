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

# Serializer para manejar la carga de imágenes y el nombre completo
class ImageUploadSerializer(serializers.Serializer):
    image = serializers.FileField(required=False, allow_null=True)
    full_name = serializers.CharField(required=True, max_length=255)  # Campo para el nombre completo
    rfc = serializers.CharField(required=True, max_length=13)  # Campo para el RFC

# Vista para extraer nombres de INE
class ImageNameExtractorView(APIView):
    parser_classes = (MultiPartParser,)
    serializer_class = ImageUploadSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        image_file = serializer.validated_data['image']
        full_name = serializer.validated_data['full_name']
        rfc = serializer.validated_data['rfc']

        return self.generate_token(rfc)
        # Convertir el archivo subido a un formato que OpenCV pueda leer
        image = np.frombuffer(image_file.read(), np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # Procesar la imagen para extraer el nombre
        name = self.process_image(image)

        if name:
            # Comprobar si el nombre extraído coincide con el nombre completo proporcionado
            if self.names_match(full_name, name):
                return self.generate_token(rfc)
            else:
                return Response({'error': 'The extracted name does not match the provided full name.'}, 
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Name not found in the text.'}, status=status.HTTP_404_NOT_FOUND)

    def process_image(self, image):
        # Recortar la imagen
        cropped_image = self.crop_image(image)

        # Extraer texto de la imagen
        extracted_text = self.extract_text_from_image(cropped_image)

        # Extraer el nombre del texto extraído
        name = self.extract_name_from_text(extracted_text)
        return name

    def crop_image(self, image):
        height, width = image.shape[:2]
        
        # Recortes para área del nombre de la INE
        left_crop_pct = 0.318   # 31.8% desde la izquierda
        top_crop_pct = 0.267    # 26.7% desde la parte superior
        right_crop_pct = 0.287  # 28.7% desde la derecha
        bottom_crop_pct = 0.446 # 44.6% desde la parte inferior

        left_crop = int(width * left_crop_pct)
        top_crop = int(height * top_crop_pct)
        right_crop = width - int(width * right_crop_pct)
        bottom_crop = height - int(height * bottom_crop_pct)

        cropped_image = image[top_crop:bottom_crop, left_crop:right_crop]
        return cropped_image

    def extract_text_from_image(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        filtered = cv2.bilateralFilter(gray, 11, 17, 17)
        thresholded = cv2.adaptiveThreshold(filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                            cv2.THRESH_BINARY, 11, 2)

        reader = easyocr.Reader(['es'], gpu=False)
        result = reader.readtext(thresholded, detail=1)
        extracted_text = ' '.join([item[1] for item in result])
        return extracted_text

    def extract_name_from_text(self, text):
        nombre_keyword = "NOMBRE"
        start_index = text.find(nombre_keyword)
        
        if start_index != -1:
            start_index += len(nombre_keyword)
            name_candidate = text[start_index:].strip()
            name_pattern = re.compile(r'^[A-ZÁÉÍÓÚÑ\s]+')
            match = name_pattern.match(name_candidate)
            if match:
                return match.group().strip()
        
        return None
    
    def generate_token(self, rfc):
        # Intentar obtener o crear un usuario con el RFC como nombre de usuario
        user, created = User.objects.get_or_create(username=rfc)

        # Si el usuario ya existe, generamos un nuevo token
        refresh = RefreshToken.for_user(user)  # Generar token para el usuario creado
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

    def names_match(self, full_name, extracted_name):
        """Compara el nombre completo proporcionado con el nombre extraído sin importar el orden."""
        # Convertir ambos nombres a conjuntos de palabras en mayúsculas
        set_full_name = set(full_name.strip().upper().split())
        set_extracted_name = set(extracted_name.strip().upper().split())
        return set_full_name == set_extracted_name  # Comparar conjuntos