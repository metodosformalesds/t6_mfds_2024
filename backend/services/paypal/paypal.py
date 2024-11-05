from datetime import timedelta
import os
import requests
import time
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework import status
from services.paypal.serializers import  PayPalProductSerializer
from database.models import Payments, Transaction, Loan, Borrower, Moneylender, ActiveLoan
from rest_framework.response import Response

CLIENT_ID_PAYPAL = os.getenv('CLIENT_ID_PAYPAL', 'Default_Secret')
SECRET_PAYPAL = os.getenv('SECRET_PAYPAL', '')
def get_paypal_access_token():
    client_id = CLIENT_ID_PAYPAL
    secret = SECRET_PAYPAL
    url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US"
    }
    response = requests.post(url, headers=headers, auth=(client_id, secret), data={"grant_type": "client_credentials"})
    return response.json().get("access_token")

class CreateCheckout(APIView):
    def post(self, request):
        print("Received request data:", request.data)

        loan_id = request.data.get("loan_id")  # Obtener el ID del préstamo de la solicitud
        print("Extracted loan_id:", loan_id)

        amount = None
        print(request.user)
        # Determinar la cantidad según el rol del usuario
        if hasattr(request.user, 'moneylender'):
            print("User is a Moneylender. Attempting to retrieve Loan.")
            try:
                loan = Loan.objects.get(id=loan_id)
                amount = loan.amount  # Obtener la cantidad directamente del préstamo
                if ActiveLoan.objects.filter(loan=loan).exists():
                    print("Error: ActiveLoan already exists for this Loan.")
                    return Response({"error": "ActiveLoan already exists for this Loan"}, status=status.HTTP_400_BAD_REQUEST)

                print("Loan found. Amount:", amount)
            except Loan.DoesNotExist:
                print("Error: Loan not found for ID:", loan_id)
                return Response({"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND)
        elif hasattr(request.user, 'borrower'):
            print("User is a Borrower. Attempting to retrieve ActiveLoan.")
            try:
                active_loan = ActiveLoan.objects.get(id=loan_id)
                if not active_loan.loan:
                    print("Error: ActiveLoan is not linked to any Loan.")
                    return Response({"error": "ActiveLoan is not linked to any Loan"}, status=status.HTTP_400_BAD_REQUEST)

                amount = active_loan.amount  # Obtener la cantidad directamente del ActiveLoan
                print("ActiveLoan found. Amount:", amount)
            except ActiveLoan.DoesNotExist:
                print("Error: ActiveLoan not found for ID:", loan_id)
                return Response({"error": "ActiveLoan not found"}, status=status.HTTP_404_NOT_FOUND)

        if amount is None:
            print("Error: Amount not found.")
            return Response({"error": "Amount not found"}, status=status.HTTP_404_NOT_FOUND)


        order_data = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": "USD",
                        "value": str(amount)  # Usar la cantidad obtenida
                    }
                }
            ]
        }

        # Obtener token de acceso llamando a la función
        access_token = get_paypal_access_token()

        # Crear la orden en PayPal
        response = requests.post(
            "https://api-m.sandbox.paypal.com/v2/checkout/orders",
            json=order_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
        )

        if response.status_code == 201:
            order_id = response.json().get("id")
            return Response({"orderID": order_id}, status=status.HTTP_201_CREATED)
        else:
            return Response(response.json(), status=response.status_code)
        
class CaptureCheckout(APIView):
    def post(self, request):
        order_id = request.data.get("orderID")
        loan_id = request.data.get("loan_id")  
        person_id = request.data.get("person_id")  

        try:
            # Obtener token de acceso 
            access_token = get_paypal_access_token()
        except Exception as e:
            return Response({"error": "Error al obtener el token de PayPal", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Inicializar amount y recipient_email
        recipient = None
        amount = None
        recipient_email = None
        loan = None
        
        try:
            # Determinar la cantidad y el correo electrónico según el rol del usuario
            if hasattr(request.user, 'moneylender'):
                # Si el usuario es Moneylender, buscar el Loan
                loan = Loan.objects.get(id=loan_id)
                amount = loan.amount  # Obtener la cantidad directamente del préstamo
                recipient = Borrower.objects.get(id=person_id)
                recipient_email = recipient.user.paypal_email  # Correo del Borrower
                
            elif hasattr(request.user, 'borrower'):
                # Si el usuario es Borrower, buscar el ActiveLoan
                loan = ActiveLoan.objects.get(id=loan_id)
                amount = loan.amount_to_pay  # Obtener la cantidad directamente del ActiveLoan
                recipient = Moneylender.objects.get(id=person_id)
                recipient_email = recipient.user.paypal_email  # Correo del Moneylender

            if amount is None:
                return Response({"error": "Amount not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except (Loan.DoesNotExist, Borrower.DoesNotExist, ActiveLoan.DoesNotExist, Moneylender.DoesNotExist) as e:
            return Response({"error": "Loan or Borrower/Moneylender not found", "details": str(e)}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Capturar el pago de la orden
            capture_url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture"
            capture_response = requests.post(
                capture_url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}"
                }
            )

            if capture_response.status_code == 201:
                # Lógica para enviar el payout
                
                # Si el usuario es un Borrower, verificar si tiene pagos pendientes
                if hasattr(request.user, 'borrower'):
                    pending_payments = Payments.objects.filter(active_loan=loan, paid=False)
                    if not pending_payments.exists():
                        return Response({"error": "El prestatario no tiene pagos pendientes."}, status=status.HTTP_400_BAD_REQUEST)

                # Intentar el payout 3 veces
                max_tries = 3
                for attempt in range(max_tries):
                    payout_info = self.send_payout(recipient_email, amount, "USD", loan, request.user)  
                    if 'error' not in payout_info:
                        if hasattr(request.user, 'moneylender'):
                            # Crear un nuevo ActiveLoan
                            new_active_loan = ActiveLoan.objects.create(
                                loan=loan,
                                borrower=recipient,
                                moneylender=request.user.moneylender,
                                total_debt_paid=0,
                                amount_to_pay=loan.amount,
                                start_date=timezone.now()
                            )
                            self.create_payment_schedule(new_active_loan)
                            self.create_transaction(new_active_loan, amount, payout_info.get('batch_header', {}).get('payout_batch_id'))

                        elif hasattr(request.user, 'borrower'):
                            most_recent_payment = Payments.objects.filter(active_loan=loan, paid=False).order_by('date_to_pay').first()
                            loan.total_debt_paid += amount
                            loan.amount_to_pay -= amount
                            loan.save()
                            most_recent_payment.paid = True
                            most_recent_payment.paid_on_time = most_recent_payment.date_to_pay >= timezone.now().date()
                            most_recent_payment.save()
                            self.create_transaction(loan, amount, payout_info.get('batch_header', {}).get('payout_batch_id'))


                        return Response({
                            "capture_info": capture_response.json(),
                            "payout_info": payout_info
                        }, status=status.HTTP_200_OK)
                    
                    # Si falla el payout, esperar un momento antes de intentar de nuevo
                    time.sleep(2)
                
                # Si después de 3 intentos el payout falla, revertir el pago capturado
                reversal_response = self.refund_payment(order_id)
                return Response({
                    "error": "Error al realizar la transacción después de múltiples intentos.",
                    "reversal_info": reversal_response
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            else:
                return Response(capture_response.json(), status=capture_response.status_code)

        except requests.RequestException as e:
            return Response({"error": "Error en la comunicación con PayPal", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": "Error inesperado", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
    def send_payout(self, recipient_email, amount, currency, loan, user):
        access_token = get_paypal_access_token()
        url = "https://api-m.sandbox.paypal.com/v1/payments/payouts"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        
        # Generar un sender_batch_id único
        sender_batch_id = f"loan_{loan.id}_user_{user.id}_{timezone.now().strftime('%Y%m%d%H%M%S')}"

        # Personalizar el mensaje según el rol del usuario
        if hasattr(user, 'moneylender'):
            note = f"Se ha enviado un pago de {amount} para el préstamo ID: {loan.id}."
        else:
            note = f"Se ha recibido un pago de {amount} para el préstamo ID: {loan.id}."

        payload = {
            "sender_batch_header": {
                "sender_batch_id": sender_batch_id, 
                "email_subject": "You have a payment"
            },
            "items": [{
                "recipient_type": "EMAIL",
                "amount": {
                    "value": str(amount),
                    "currency": currency
                },
                #Cambiar a la variable recipient_email (cambiar el modelo de user para agregar paypal email)
                "receiver": recipient_email,
                "note": note,
                "sender_item_id": f"item_{loan.id}"
            }]
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            payout_info = response.json()
            return payout_info
        else:
            return {"error": response.json()}
        
    def refund_payment(self, order_id):
        access_token = get_paypal_access_token()
        refund_url = f"https://api-m.sandbox.paypal.com/v2/payments/captures/{order_id}/refund"
        response = requests.post(
            refund_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
        )
        return response.json() if response.status_code == 201 else {"error": response.json()}
        
    def create_transaction(self, active_loan, amount, paypal_transaction_id):
        """Crea una transacción relacionada con el ActiveLoan."""
        Transaction.objects.create(
            active_loan=active_loan,  # Relacionar la transacción con el ActiveLoan
            amount_paid=amount,
            paypal_transaction_id=paypal_transaction_id,  # ID de la transacción de PayPal
            status='completed',  # Estado de la transacción
            transaction_type='payment'  # Tipo de transacción
        )
   
    def create_payment_schedule(self, active_loan):
        # Generate scheduled payments based on loan terms
        interval = {
            1: timedelta(weeks=1),  # Weekly
            2: timedelta(weeks=2),  # Biweekly
            3: timedelta(weeks=4),  # Monthly
        }.get(active_loan.loan.term, timedelta(weeks=4))

        for number in range(1, active_loan.loan.number_of_payments + 1):
            date_to_pay = active_loan.start_date + (interval * number)
            Payments.objects.create(
                active_loan=active_loan,
                number_of_pay=number,
                date_to_pay=date_to_pay,
                paid=False,
                paid_on_time=None  # This can be updated later based on payment status
            )

        
class CreatePayPalProductView(APIView):  
    serializer_class = PayPalProductSerializer
    def post(self, request, *args, **kwargs):
        serializer = PayPalProductSerializer(data=request.data)
        
        if serializer.is_valid():
            access_token = get_paypal_access_token()
            if not access_token:
                return Response({"error": "Could not retrieve PayPal access token"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            url = "https://api-m.sandbox.paypal.com/v1/catalogs/products"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
                "PayPal-Request-Id": "REQUEST-ID"
            }
            response = requests.post(url, headers=headers, json=serializer.validated_data)

            if response.status_code == 201:
                return Response(response.json(), status=status.HTTP_201_CREATED)
            else:
                return Response(response.json(), status=response.status_code)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CreatePayPalBillingPlanView(APIView):

    def post(self, request, *args, **kwargs):
        
        access_token = get_paypal_access_token()
        if not access_token:
            return Response({"error": "Could not retrieve PayPal access token"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        url = "https://api-m.sandbox.paypal.com/v1/billing/plans"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
            "PayPal-Request-Id": "12"
        }

       
        data = {
        "product_id": "PROD-3G8497537T6075127",
        "name": "LlamasCoin Subscription Plan",
        "billing_cycles": [
            {
                "tenure_type": "REGULAR",
                "sequence": 1,
                "frequency": {
                    "interval_unit": "MONTH",
                    "interval_count": 1
                },
                "total_cycles": 12,
                "pricing_scheme": {
                    "fixed_price": {
                        "value": "50",
                        "currency_code": "USD"
                    }
                }
            }
        ],
        "payment_preferences": {
            "auto_bill_outstanding": True,
            "setup_fee": {
                "value": "0",
                "currency_code": "USD"
            },
            "setup_fee_failure_action": "CONTINUE",
            "payment_failure_threshold": 3
        },
        "description": "Plan plus para el servicio de prestamos",
        "status": "ACTIVE",
        "taxes": {
            "percentage": "10",
            "inclusive": False
        }
    }
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 201:
            return Response(response.json(), status=status.HTTP_201_CREATED)
        else:
            return Response(response.json(), status=response.status_code)

  