import os
import django
import sys

# Obtén la ruta absoluta del directorio raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'llamascoin.settings')
django.setup()

from send_mail import EmailSender  # Importa la clase EmailSender

# Solicita los datos de forma dinámica
destinatario = input("Ingrese el correo del destinatario: ")
asunto = input("Ingrese el asunto del correo: ")
template_name = input("Ingrese la plantilla a utilizar: ")
nombre = input("Ingrese el nombre del destinatario: ")

# Instancia y usa la clase EmailSender
email_sender = EmailSender(
    recipient=destinatario,
    subject=asunto,
    template_name=template_name,
    name=nombre
)

# Llama al método para enviar el correo
email_sender.send_email()
