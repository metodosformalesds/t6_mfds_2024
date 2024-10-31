from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage,get_connection,send_mass_mail
from django.utils.html import strip_tags


def simple_mail(request):
    try:
        send_mail(
            subject='Hola desde Django',
            message='Este es un mensaje de prueba usando Mailtrap.',
            from_email='u21210757@utp.edu.pe',
            recipient_list=['u21210757@utp.edu.pe'],
            fail_silently=False,  # Lanza excepciones si hay un error
        )
        return HttpResponse('Mensaje Enviado')
    except Exception as e:
        # Manejo de la excepción
        return HttpResponse(f'Ocurrió un error al enviar el correo: {str(e)}')

def html(request):
    subject='envio'
    html_message=render_to_string('plantillas/envio.html',{'message':'prueba'})
    plain_message=strip_tags(html_message)
    from_email='u21210757@utp.edu.pe'
    to='a@gmail.com'
    send_mail(subject,plain_message,from_email, [to],html_message=html_message)
    return HttpResponse('Mensaje Enviado')

