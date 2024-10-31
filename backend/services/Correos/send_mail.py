from django.core.mail import send_mail
from django.http import HttpResponse

def simple_mail(request):
    try:
        send_mail(
            subject='Hola desde Django',
            message='Este es un mensaje de prueba usando Mailtrap.',
            from_email='u21210757@utp.edu.pe',
            recipient_list=['u21210757@utp.edu.pe'],
            fail_silently=False  # Lanza excepciones si hay un error
        )
        return HttpResponse('Mensaje Enviado')
    except Exception as e:
        # Manejo de la excepción
        return HttpResponse(f'Ocurrió un error al enviar el correo: {str(e)}')