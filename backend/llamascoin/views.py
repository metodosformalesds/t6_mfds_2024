from rest_framework.decorators import api_view 
from rest_framework.response import Response
from .serializers import UserSerializer, UserRegistrationSerializer, UserLoginSerializer
from database.serializers import BorrowerSerializer, MoneylenderSerializer, RequestSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from database.models import ActiveLoan, Payments, Request, User, Moneylender, Borrower, CreditHistory
from services.filters import requestfilter
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.utils import timezone
from services.Correos.send_mail import EmailSender
from rest_framework.permissions import IsAuthenticated, AllowAny

#Vista para registrar el usuario
class RegisterView(APIView):
    """
    Vista para registrar un usuario provisional en el sistema.

    Esta vista maneja solicitudes POST para registrar nuevos usuarios. La información del usuario es validada
    a través del `UserRegistrationSerializer`. Si los datos son válidos, se crea un usuario provisional en la 
    base de datos con la contraseña hasheada.

    Args:
        APIView: Clase base para vistas basadas en API en Django Rest Framework.

    Atributos:
        serializer_class (class): Clase de serializador utilizada para validar los datos de entrada.
        permission_classes (list): Lista de permisos que define quién puede acceder a esta vista.

    Métodos:
        post(request):
            Maneja solicitudes POST para registrar un nuevo usuario.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        """
        Maneja solicitudes POST para registrar un nuevo usuario provisional.

        Procesa la información enviada por el cliente, la valida y crea un usuario provisional en la base 
        de datos con los siguientes campos: `email`, `paypal_email`, `curp`, `account_type` y una contraseña 
        hasheada. Si los datos son inválidos, responde con un error.

        Args:
            request (HttpRequest): La solicitud HTTP enviada al servidor.

        Returns:
            Response: 
                - `HTTP_201_CREATED` si el usuario se registra correctamente.
                - `HTTP_400_BAD_REQUEST` si los datos enviados son inválidos.
        """
        serializer = UserRegistrationSerializer(data=request.data)
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
            # Si los datos son inválidos
            return Response(
                {"error": "Datos inválidos", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            
#Vista para resivir form.procedded.succes y registar los datos del formulario
@csrf_exempt
def Formulario(request):
    """
    Procesa una solicitud POST para actualizar o crear información de usuario basado en el CURP.

    Esta función permite actualizar o crear registros en los modelos `Moneylender` o `Borrower`, dependiendo
    del tipo de cuenta del usuario asociado. Los datos son enviados en formato JSON en el cuerpo de la 
    solicitud POST. La función realiza las siguientes acciones:

    1. Valida que el método de la solicitud sea POST.
    2. Convierte el cuerpo de la solicitud a un diccionario Python.
    3. Busca al usuario en la base de datos utilizando el CURP proporcionado.
    4. Si el usuario no existe, responde con un error.
    5. Dependiendo del tipo de cuenta (`moneylender` o `borrower`), actualiza o crea registros en los modelos correspondientes.
    6. Devuelve un estado exitoso o un mensaje de error en caso de fallo.

    Args:
        request (HttpRequest): La solicitud HTTP enviada al servidor.

    Returns:
        JsonResponse: Una respuesta JSON que indica el estado del procesamiento.
    """
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
    """
    Valida la identidad de un usuario y actualiza o elimina su información basada en la respuesta de Jumio.

    Esta función recibe una solicitud POST con datos en formato JSON, incluyendo el estado de validación y el CURP
    del usuario. Dependiendo del estado, realiza las siguientes acciones:

    - Si el estado es 'SUCCESS', marca al usuario como verificado (`is_verified = True`) y lo guarda.
    - Si el estado es 'FAIL', elimina al usuario de la base de datos.
    - Si el usuario es del tipo `borrower`, realiza una consulta a una API externa (Moffin) para generar un historial crediticio,
      el cual se almacena en el modelo `CreditHistory`.

    Args:
        request (HttpRequest): La solicitud HTTP enviada al servidor.

    Returns:
        JsonResponse: Una respuesta JSON que indica el estado del procesamiento.
    """
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
        #user = User.objects.filter(curp=curp).first()
        user = User.objects.get(curp=curp)
        user_id = user.id
        print("user:", user_id)
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
        
        
        if user.account_type == 'borrower':
            borrower = Borrower.objects.get(user_id=user_id)
            datos = {    
                'firstName': borrower.first_name,
                'firstLastName': borrower.first_name,
                'secondLastName': borrower.second_surname,
                'rfc': borrower.rfc,
                'birthdate': borrower.birth_date,
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
            
            api_url = "https://sandbox.moffin.mx/api/v1/query/bureau_pf"
            headers = {
                'Authorization': 'Token d0a8721978878bd705228203826fa9178a1f2c496db20e4402f92ff84b2b3379',
                'Content-Type': 'application/json'
            }

            try:
                # Hacer la solicitud POST a la API externa
                api_response = requests.post(api_url, json=datos, headers=headers)
                api_response.raise_for_status()
                api_data = api_response.json()

                resumen_data = (api_data.get("response", {}).get("return", {}).get("Personas", {}).get("Persona", [{}])[0] .get("ResumenReporte", {}).get("ResumenReporte", [{}])[0] )
                score_data = (api_data.get("response", {}).get("return", {}).get("Personas", {}).get("Persona", [{}])[0].get("ScoreBuroCredito", {}).get("ScoreBC", [{}])[0]) 
                
                credit_history = CreditHistory(
                    
                    borrower=borrower,
                    date_account_open = timezone.now(),
                    check_date = timezone.now(),
                    accounts_open=int(resumen_data.get('NumeroCuentas', 0)),
                    accounts_closed=int(resumen_data.get('CuentasCerradas', 0)),
                    negative_accounts=int(resumen_data.get('CuentasNegativasActuales', 0)),
                    num_mop1=int(resumen_data.get('NumeroMOP1', 0)),
                    num_mop2=int(resumen_data.get('NumeroMOP2', 0)),
                    num_mop3=int(resumen_data.get('NumeroMOP3', 0)),
                    num_mop4=int(resumen_data.get('NumeroMOP4', 0)),
                    num_mop5=int(resumen_data.get('NumeroMOP5', 0)),
                    num_mop6=int(resumen_data.get('NumeroMOP6', 0)),
                    num_mop7=int(resumen_data.get('NumeroMOP7', 0)),
                    num_mop99=int(resumen_data.get('NumeroMOP99', 0)),
                    code_score=(score_data.get('CodigoScore', 0)), 
                    val_score=(score_data.get('Valorscore', 0)),
                )
                
                credit_history.save()
                
                try:
                    recipient = user.email
                    subject = "Validación y registro en LlamasCoin exitoso"
                    template_name = "envio.html"
                    name = borrower.first_name + " " + borrower.first_surname + " " + borrower.second_surname
                    # Crea una instancia de EmailSender
                    email_sender = EmailSender(recipient, subject, template_name, {"nombre": name})
                    
                    # Envía el correo
                    email_sender.send_email()

                except Exception as e:
                    print(f"Error al enviar el correo de registro: {e}")

             
                return JsonResponse({"status": "Data processed successfully"})
            except requests.exceptions.RequestException:
                return JsonResponse({"error": "API request failed"}, status=500)
            except KeyError:
                return JsonResponse({"error": "Missing data in API response"}, status=500)
    
        return JsonResponse({"status": "Data processed successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=405)
        
class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = requestfilter


class LoginView(APIView):
    """
    Vista para el inicio de sesión de usuarios.

    Permite a los usuarios autenticarse en el sistema utilizando su correo electrónico y contraseña. 
    Devuelve un token JWT con información adicional sobre el usuario si la autenticación es exitosa.

    Atributos:
        serializer_class (Serializer): Clase del serializador utilizada para validar y procesar los datos.
        permission_classes (list): Lista de permisos necesarios para acceder a esta vista.
    """

    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Maneja solicitudes POST para iniciar sesión.

        Este método:
        - Busca al usuario utilizando el correo electrónico proporcionado en lugar del nombre de usuario.
        - Verifica la contraseña del usuario.
        - Comprueba si la cuenta del usuario está verificada.
        - Si todo es válido, genera un token JWT con información adicional sobre el usuario, como su correo electrónico, rol y ID.
        - Si la autenticación falla, devuelve un mensaje de error.

        Args:
            request (Request): Objeto de solicitud HTTP con los datos enviados.

        Returns:
            Response: Respuesta HTTP con uno de los siguientes estados:
                - 200 OK: Cuando el inicio de sesión es exitoso, incluye el token JWT y datos del usuario.
                - 400 Bad Request: Cuando la contraseña es incorrecta.
                - 401 Unauthorized: Cuando el usuario no está verificado y se elimina su registro.
        """
        # Buscar el usuario por correo electrónico en lugar de nombre de usuario
        user = get_object_or_404(User, email=request.data['username'])
        
        # Validar la contraseña
        if not user.check_password(request.data['password']):
            return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_verified:
            user.delete()
            return Response({"error": "No se pudo validar su identidad correctamente, inice el registro nuevamente"}, status=status.HTTP_401_UNAUTHORIZED)
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

from datetime import datetime
SECRET_API_KEY= "Llamascoin!098"


class DailyCheckView(APIView):
    """
    View to perform a daily check of pending payments and send email notifications
    to borrowers with upcoming or overdue payments.

    This endpoint accepts a POST request and performs the following actions:
    1. Validates the API key provided in the request body.
    2. Retrieves all pending payments associated with active loans.
    3. Calculates the number of days remaining until the payment due date for each pending loan.
    4. Sends an email reminder based on the number of days remaining:
        - 5, 3, 1, or 0 days before the due date sends a payment reminder.
        - If the due date has passed (negative days), an overdue payment reminder is sent.
    5. Returns a JSON response indicating the status of the process and the number of notifications sent.

    Attributes:
        None

    Methods:
        post(request, *args, **kwargs):
            Handles POST requests to perform the payment check and send notifications.

    """
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        api_key = request.data.get("key")
        if api_key != SECRET_API_KEY:
            return JsonResponse({"error": "Invalid API key"}, status=403)

        today = datetime.now().date()
        notifications = []

        # Optimización: Obtener todos los pagos de una vez
        payments = Payments.objects.filter(paid=False).select_related('active_loan').order_by('date_to_pay')

        # Iterar solo por préstamos activos
        for active_loan in ActiveLoan.objects.all():
            borrower_email = active_loan.borrower.user.email

            # Filtrar pagos asociados al préstamo actual
            loan_payments = payments.filter(active_loan=active_loan)

            if loan_payments.exists():
                # Tomamos el primer pago pendiente
                first_pending_payment = loan_payments.first()
                days_left = (first_pending_payment.date_to_pay - today).days

                print(f"Processing ActiveLoan ID: {active_loan.id}")
                print(f"Borrower Email: {borrower_email}")
                print(f"First Pending Payment ID: {first_pending_payment.id}")
                print(f"Date to Pay: {first_pending_payment.date_to_pay}, Paid: {first_pending_payment.paid}")
                print(f"Days left for Payment ID {first_pending_payment.id}: {days_left}")

                # Lógica para notificaciones y asignación de plantilla
                if days_left in [5, 3, 1, 0]:
                    # Usamos "recordatorio-pagar.html" para 5, 3, 1 y 0 días
                    template_name = "recordatorio-pagar.html"
                elif days_left == -1:
                    # Usamos "recordatorio-pasado.html" para el caso de días pasados
                    template_name = "recordatorio-pasado.html"
                else:
                    continue  # Si no es un día relevante, no se envía nada

                # Añadir la notificación con los detalles correspondientes
                notifications.append({
                    "borrower_email": borrower_email,
                    "days_left": days_left,
                    "template": template_name,
                    "context": {
                        'nombre_prestamista': active_loan.borrower.first_name,
                        'fecha_pago': first_pending_payment.date_to_pay,
                    }
                })

        # Enviar notificaciones
        for notification in notifications:
            try:
                email_sender = EmailSender(
                    recipient=notification["borrower_email"],
                    subject="Recordatorio de pago",
                    template_name=notification["template"],
                    context=notification["context"]
                )
                email_sender.send_email()
                print(f"Email sent to {notification['borrower_email']} for {notification['days_left']} days left.")
            except Exception as e:
                print(f"Error sending email to {notification['borrower_email']}: {e}")

        return JsonResponse({"status": "Daily check completed", "notifications_sent": len(notifications)})