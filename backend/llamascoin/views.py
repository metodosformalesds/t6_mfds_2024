from rest_framework.decorators import api_view 
from rest_framework.response import Response
from .serializers import UserSerializer, UserRegistrationSerializer
from database.serializers import BorrowerSerializer, MoneylenderSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
class LoginView(APIView):
    def post(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        
        if not user.check_password(request.data['password']):
            return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Crear el token JWT
        refresh = RefreshToken.for_user(user)
        
        # Incluir datos adicionales en el token
        token_data = {
            'username': user.username,
            'role': 'borrower' if hasattr(user, 'borrower') else 'moneylender' if hasattr(user, 'moneylender') else 'user',
            'user_id': user.id,
        }
        
        refresh['username'] = token_data['username']
        refresh['role'] = token_data['role']
        refresh['user_id'] = token_data['user_id']
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': token_data['username'],
            'role': token_data['role'],
            'user_id': token_data['user_id'],
        }, status=status.HTTP_200_OK)
        
class RegisterView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_serializer = UserRegistrationSerializer(data=request.data)

        if user_serializer.is_valid():
            validated_data = user_serializer.validated_data
            
           # Verificar si el usuario ya existe
            if User.objects.filter(username=validated_data['username']).exists():
                return Response({'username': 'Este nombre de usuario ya está en uso.'}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(email=validated_data['email']).exists():
                return Response({'email': 'Este correo electrónico ya está registrado.'}, status=status.HTTP_400_BAD_REQUEST)

            # Crear el objeto User
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
            
            # Manejar account_type
            account_type = validated_data['account_type']
            rfc = None
            
            if account_type == 'borrower':
                borrower_data = request.data.get('borrower')
                borrower_data['user'] = user.id
                rfc = borrower_data.get('rfc')
                borrower_serializer = BorrowerSerializer(data=borrower_data)
                if borrower_serializer.is_valid():
                    borrower_serializer.save(user=user)
                else:
                    user.delete()  # Eliminar el usuario si falla la creación del borrower
                    return Response(borrower_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif account_type == 'moneylender':
                moneylender_data = request.data.get('moneylender')
                moneylender_data['user'] = user.id
                rfc = moneylender_data.get('rfc') 
                moneylender_serializer = MoneylenderSerializer(data=moneylender_data)
                if moneylender_serializer.is_valid():
                    moneylender_serializer.save(user=user)
                else:
                    user.delete()  # Eliminar el usuario si falla la creación del moneylender
                    return Response(moneylender_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Borrar el usuario que se creó con el RFC en la validación de la INE
            if rfc:  # Solo intentamos eliminar si se obtuvo un RFC
                try:
                    user_to_delete = User.objects.get(username=rfc) 
                    user_to_delete.delete()
                except User.DoesNotExist:
                    pass
                
                
             # Crear el token JWT
            refresh = RefreshToken.for_user(user)

            # Incluir datos adicionales en el token
            token_data = {
                'username': user.username,
                'role': 'borrower' if account_type == 'borrower' else 'moneylender',
                'user_id': user.id,
            }
                
            refresh['username'] = token_data['username']
            refresh['role'] = token_data['role']
            refresh['user_id'] = token_data['user_id']

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': token_data['username'],
                'role': token_data['role'],
                'user_id': token_data['user_id'],
            }, status=status.HTTP_201_CREATED)
            

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

