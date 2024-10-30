from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

# Serializer para manejar la carga de imágenes y el nombre completo
class ImageUploadSerializer(serializers.Serializer):
    
    #Ajustar para la informacion que la API requiere
    
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

        #Logica de la llamada a la API y validar respuestas para responder con el token generado
        

        return self.generate_token(rfc)
        
    
    def generate_token(self, rfc):
        # Intentar obtener o crear un usuario con el RFC como nombre de usuario
        user, created = User.objects.get_or_create(username=rfc)

        # Si el usuario ya existe, generamos un nuevo token
        refresh = RefreshToken.for_user(user)  # Generar token para el usuario creado
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
