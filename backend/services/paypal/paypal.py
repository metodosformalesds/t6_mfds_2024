import os
import requests
from rest_framework.views import APIView
from rest_framework import status
from services.paypal.serializers import PaymentSerializer, PayoutSerializer, PayPalProductSerializer
from database.models import Transaction
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

class CreatePaymentView(APIView):
    serializer_class = PaymentSerializer
    def post(self, request):
    
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            access_token = get_paypal_access_token()
            url = "https://api-m.sandbox.paypal.com/v1/payments/payment"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
            payload = {
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "redirect_urls": {
                    "return_url": "http://127.0.0.1:8000/paypal/return/",
                    "cancel_url": "http://127.0.0.1:8000/paypal/cancel/"
                },
                "transactions": [{
                    "amount": {
                        "total": str(serializer.validated_data['amount']),
                        "currency": serializer.validated_data['currency']
                    },
                    "description": "Descripción del producto o servicio"
                }]
            }

            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 201:
                payment_info = response.json()
                return Response({"payment_id": payment_info['id'], "links": payment_info['links']}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": response.json()}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendPayoutView(APIView):
    serializer_class = PayoutSerializer

    def post(self, request):
        serializer = PayoutSerializer(data=request.data)
        if serializer.is_valid():
            access_token = get_paypal_access_token()
            url = "https://api-m.sandbox.paypal.com/v1/payments/payouts"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
            payload = {
                "sender_batch_header": {
                    "sender_batch_id": "batch_225",  # Debe ser único
                    "email_subject": "You have a payment"
                },
                "items": [{
                    "recipient_type": "EMAIL",
                    "amount": {
                        "value": str(serializer.validated_data['amount']),
                        "currency": serializer.validated_data['currency']
                    },
                    "receiver": serializer.validated_data['recipient_email'],
                    "note": "Gracias por tu negocio.",
                    "sender_item_id": "item_1"
                }]
            }

            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 201:
                payout_info = response.json()
                print(payout_info)
                payment_status = payout_info['batch_header']['batch_status']  # Actualiza según tu respuesta
                # Registrar el payout en la base de datos
                Transaction.objects.create(
                    ID_ActiveLoan=serializer.validated_data['active_loan_id'],  # Asigna el ID del préstamo activo
                    AmountPaid=float(serializer.validated_data['amount']),
                    PayPalTransactionID=payout_info['batch_header']['payout_batch_id'],  # Usa el ID de batch de payout
                    Status=payment_status,
                    TransactionType='payout'  # O 'income' según corresponda
                )
                return Response({"payout_info": payout_info}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": response.json()}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PayPalReturnView(APIView):
    
    def get(self, request):
        # Obtener los parámetros de la consulta
        payment_id = request.query_params.get('paymentId')
        payer_id = request.query_params.get('PayerID')

        # Imprimir los parámetros recibidos
        print("Payment ID:", payment_id)
        print("Payer ID:", payer_id)

        # Confirmar el pago con PayPal
        access_token = get_paypal_access_token()
        print("Access Token:", access_token)

        # URL para ejecutar el pago
        url = f"https://api-m.sandbox.paypal.com/v1/payments/payment/{payment_id}/execute"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        payload = {
            "payer_id": payer_id
        }

        # Realizar la solicitud para ejecutar el pago
        response = requests.post(url, headers=headers, json=payload)

        # Imprimir el código de estado y la respuesta de PayPal
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.json())

        if response.status_code == 200:
            # Procesar el pago exitosamente
            payment_info = response.json()
            # Registrar el pago en la base de datos
            Transaction.objects.create(
                ID_ActiveLoan=payment_info['transactions'][0]['item_list']['items'][0]['id'], 
                AmountPaid=float(payment_info['transactions'][0]['amount']['total']),
                PayPalTransactionID=payment_info['id'],
                Status='completed',  # Marca el pago como completado
                TransactionType='income'  # O 'payout' según corresponda
            )
            return Response({"message": "Pago exitoso", "payment_info": payment_info}, status=status.HTTP_200_OK)
        else:
            return Response({"error": response.json()}, status=status.HTTP_400_BAD_REQUEST)
class PayPalCancelView(APIView):
    def get(self, request):
        return Response({"message": "Pago cancelado"}, status=status.HTTP_200_OK)



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

  