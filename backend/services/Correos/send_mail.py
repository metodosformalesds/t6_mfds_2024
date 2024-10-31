import os
import django
import sys

# Obtén la ruta absoluta del directorio raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Agrega el directorio raíz del proyecto al sys.path
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'llamascoin.settings')
django.setup()

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Define la función para enviar correos
def enviar_email_html(asunto, plantilla_html, contexto, remitente, destinatario):
    html_message = render_to_string(plantilla_html, contexto)
    plain_message = strip_tags(html_message)
    send_mail(
        subject=asunto,
        message=plain_message,
        from_email=remitente,
        recipient_list=[destinatario],
        html_message=html_message
    )
    print("Correo enviado correctamente.")

# Solicitar datos de forma dinámica
asunto = input("Ingrese el asunto del correo: ")
plantilla_html = input('plantilla:')
contexto = {}
contexto['message'] = input("Ingrese el usuario para el correo: ")
remitente = input("Ingrese el correo del remitente: ")
destinatario = input("Ingrese el correo del destinatario: ")

# Llama a la función para enviar el correo con los datos ingresados
enviar_email_html(asunto, plantilla_html, contexto, remitente, destinatario)
