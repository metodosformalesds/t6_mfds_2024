from rest_framework.decorators import api_view 
from rest_framework.response import Response
from .serializers import UserSerializer, UserRegistrationSerializer, UserLoginSerializer
from database.serializers import BorrowerSerializer, MoneylenderSerializer, RequestSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from database.models import Request, User, Moneylender, Borrower
from services.filters import requestfilter
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


#Vista para registrar el usuario
class RegisterView(APIView):
    serializer_class = UserSerializer
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Extraer los datos validados
            email = serializer.validated_data['email']
            paypal_email = serializer.validated_data['paypal_email']
            password = serializer.validated_data['password']
            curp = serializer.validated_data['curp']
            account_type = serializer.validated_data['account_type']

            # Crear el usuario provisional
            user = User(
                email=email,
                paypal_email=paypal_email,
                curp=curp,
                account_type=account_type
            )
            user.set_password(password)  # Hashear la contraseña
            user.save()

            return Response({"message": "Usuario registrado exitosamente"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#Vista para resivir form.procedded.succes y registar los datos del formulario
@csrf_exempt
def Formulario(request):
    if request.method == 'POST':
        try:
            # Convierte el cuerpo de la solicitud en un diccionario Python
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        curp = data.get('curp')
        print("CURP:", curp)
        # Verifica si el usuario existe con el CURP
        user = User.objects.filter(curp=curp).first()

        if not user:
            return JsonResponse({"error": "User not found"}, status=404)
        accountType = user.account_type
        print("Account type:", accountType)

        # Procesa según el tipo de cuenta
        if accountType == 'moneylender':  # Tipo de cuenta para Moneylender
            Moneylender.objects.update_or_create(
                user=user,
                defaults={
                    'first_name': data.get('firstName', '').strip(),
                    'middle_name': data.get('middleName', '').strip(),
                    'first_surname': data.get('firstLastName', '').strip(),
                    'second_surname': data.get('secondLastName', '').strip(),
                    'birth_date': data.get('birthdate', '').strip(),
                    'phone_number': data.get('phone'),
                    'rfc': data.get('rfc'),
                    'full_address': data.get('address'),
                    'city': data.get('city'),
                    'neighborhood': data.get('neighborhood'),
                    'postal_code': data.get('zipCode'),
                    'state': data.get('state'),
                    'country': data.get('country'),
                    'municipality': data.get('municipality'),
                    'nationality': data.get('nationality', 'MX'),
                }
            )
        elif accountType == 'borrower':  # Tipo de cuenta para Borrower
            Borrower.objects.update_or_create(
                user=user,
                defaults={
                    'first_name': data.get('firstName', '').strip(),
                    'middle_name': data.get('middleName', '').strip(),
                    'first_surname': data.get('firstLastName', '').strip(),
                    'second_surname': data.get('secondLastName', '').strip(),
                    'birth_date': data.get('birthdate', '').strip(),
                    'phone_number': data.get('phone'),
                    'rfc': data.get('rfc'),
                    'full_address': data.get('address'),
                    'city': data.get('city'),
                    'neighborhood': data.get('neighborhood'),
                    'postal_code': data.get('zipCode'),
                    'state': data.get('state'),
                    'country': data.get('country'),
                    'municipality': data.get('municipality'),
                    'nationality': data.get('nationality', 'MX'),
                }
            )
        else:
            return JsonResponse({"error": "Unknown account type"}, status=400)

        return JsonResponse({"status": "Data processed successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=405)

#Vista para resivir la validacion de identidad y validar el usuario o eliminarlo
@csrf_exempt
def jumioValidation(request):
    if request.method == 'POST':
        try:
            # Convierte el cuerpo de la solicitud en un diccionario Python
            data = json.loads(request.body)
            
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        status = data.get('status')
        curp = data.get('response', {}).get('flow', {}).get('extraction', {}).get('curp')
        print("CURP:", curp)
        print("STATUS:", status)
        # Verifica si el usuario existe con el CURP
        user = User.objects.filter(curp=curp).first()

        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        # Si la respuesta es SuCCES cambiar el atributo is_verified a True 
        if status == 'SUCCESS': 
            user.is_verified = True
            user.save()
        # Si la respuesta es FAIL borrar el usuario completo de la base de datos
        elif status == 'FAIL':  
            user.is_verified = False
            user.save()
            user.delete()
            return JsonResponse({"status": "User deleted"})
        else:
            return JsonResponse({"error": "Status no encontrado"}, status=400)

        return JsonResponse({"status": "Data processed successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=405)
        
class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = requestfilter


class LoginView(APIView):
    serializer_class = UserLoginSerializer
    
    def post(self, request):
        # Buscar el usuario por correo electrónico en lugar de nombre de usuario
        user = get_object_or_404(User, email=request.data['username'])
        
        # Validar la contraseña
        if not user.check_password(request.data['password']):
            return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Crear el token JWT
        refresh = RefreshToken.for_user(user)
        
        # Incluir datos adicionales en el token
        token_data = {
            'email': user.email,
            'role': 'borrower' if hasattr(user, 'borrower') else 'moneylender' if hasattr(user, 'moneylender') else 'user',
            'user_id': user.id,
        }
        
        # Añadir datos adicionales en el token
        refresh['email'] = token_data['email']
        refresh['role'] = token_data['role']
        refresh['user_id'] = token_data['user_id']
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'email': token_data['email'],
            'role': token_data['role'],
            'user_id': token_data['user_id'],
        }, status=status.HTTP_200_OK)

'''
class RegisterView(APIView):
    serializer_class = UserRegistrationSerializer
    #permission_classes = [IsAuthenticated]
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
'''
