from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
import cv2
import easyocr
import re
import numpy as np
from rest_framework import serializers

# Serializer para manejar la carga de imágenes
class ImageUploadSerializer(serializers.Serializer):
    image = serializers.FileField(required=False, allow_null=True)

# Vista para extraer nombres de ine
class ImageNameExtractorView(APIView):
    parser_classes = (MultiPartParser,)
    serializer_class = ImageUploadSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        image_file = serializer.validated_data['image']

        # Convertir el archivo subido a un formato que OpenCV pueda leer
        image = np.frombuffer(image_file.read(), np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # Procesar la imagen para extraer el nombre
        name = self.process_image(image)

        if name:
            return Response({'name': name}, status=status.HTTP_200_OK)
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
        
        #Recortes para area del nombre de la INE
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
