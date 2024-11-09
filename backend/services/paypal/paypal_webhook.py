import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from services.Correos.send_mail import EmailSender
from database.models import  Moneylender
from database.models import User

@csrf_exempt
@require_POST
def PayPalWebhook(request):
    # Parse the JSON payload
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    event_type = data.get('event_type')
    email = None

    # Extract email based on event type
    if event_type == 'BILLING.SUBSCRIPTION.CREATED':
        email = data.get('resource', {}).get('payer', {}).get('payer_info', {}).get('email')
    elif event_type in ['BILLING.SUBSCRIPTION.ACTIVATED', 'BILLING.SUBSCRIPTION.EXPIRED']:
        email = data.get('resource', {}).get('subscriber', {}).get('email_address')
    elif event_type == 'BILLING.SUBSCRIPTION.CANCELLED':
        email = data.get('resource', {}).get('payer', {}).get('payer_info', {}).get('email')

    # If no email is found in the event, return an error
    if not email:
        return JsonResponse({'status': 'error', 'message': 'Email not found in event'}, status=400)

    # Retrieve User instance associated with the paypal_email
    try:
        user = User.objects.get(paypal_email=email)
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

    # Retrieve Moneylender instance associated with the User
    moneylender = get_object_or_404(Moneylender, user=user)

    # Concatenate the full name from Moneylender
    user_name = f"{moneylender.first_name} {moneylender.middle_name} {moneylender.first_surname} {moneylender.second_surname}"

    # Define a base context for the email
    context = {
        'user_name': user_name,
        'email': user.email,
    }

    # Define event-specific details
    if event_type == 'BILLING.SUBSCRIPTION.CREATED':
        moneylender.is_subscribed = True
        subject = "¡Suscripción Creada!"
        event_title = "¡Suscripción Creada!"
        event_message = "Tu suscripción ha sido creada exitosamente."
        template_name = "suscripcion_activada.html"
    elif event_type == 'BILLING.SUBSCRIPTION.ACTIVATED':
        moneylender.is_subscribed = True
        subject = "¡Suscripción Activada!"
        event_title = "¡Suscripción Activada!"
        event_message = "Tu suscripción ha sido activada exitosamente."
        template_name = "suscripcion_activada.html"
    elif event_type == 'BILLING.SUBSCRIPTION.EXPIRED':
        moneylender.is_subscribed = False
        subject = "Suscripción Expirada"
        event_title = "Suscripción Expirada"
        event_message = "Tu suscripción ha expirado."
        template_name = "suscripcion_desactivada.html"
    elif event_type == 'BILLING.SUBSCRIPTION.CANCELLED':
        moneylender.is_subscribed = False
        subject = "Suscripción Cancelada"
        event_title = "Suscripción Cancelada"
        event_message = "Tu suscripción ha sido cancelada."
        template_name = "suscripcion_desactivada.html"
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid event type'}, status=400)

    # Save the updated subscription status
    moneylender.save()

    # Update context with event-specific details
    context.update({
        'event_title': event_title,
        'event_message': event_message
    })

    # Send the email
    email_sender = EmailSender(
        recipient=user.email,
        subject=subject,
        template_name=template_name,
        context=context
    )
    email_sender.send_email()

    return JsonResponse({'status': 'success', 'message': f'Subscription {event_type.split(".")[-1].lower()}'})