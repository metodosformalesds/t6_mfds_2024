import os
import django
import sys
"""
Envia datos de envío mediante consola para realizar pruebas
        Parámetros:
            recipien: Recibe el correo que recibirá el mensaje
            Subject:  Recibe el asunto del mensaje
            Template_name: Recibe la plantilla que se va a utilizar
            Context: Brinda los parametros adicioanles que se usarán en la plantilla

        Proceso:
            - Se ejecuta mediante consola para realizar pruebas de plantillas, 
               este recibe el correo del destinatario, el asunto, el template y el nombre del usuario para utilizarlo en la plantilla de bienvenida.
        Retorna:    
            Un mensaje en consola de que el mensaje se envió de forma exitosa.
"""
# Obtén la ruta absoluta del directorio raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'llamascoin.settings')
django.setup()

# Importa la clase EmailSender desde la ubicación correcta
from send_mail import EmailSender

# Solicita los datos de forma dinámica
destinatario = input("Ingrese el correo del destinatario: ")
asunto = input("Ingrese el asunto del correo: ")
template_name = input("Ingrese la plantilla a utilizar: ")
nombre = input("Ingrese el nombre del destinatario: ")

# Instancia y usa la clase EmailSender con el contexto necesario
email_sender = EmailSender(
    recipient=destinatario,
    subject=asunto,
    template_name=template_name,
    context={
        'nombre': nombre
        }  # Agrega el contexto
)

# Llama al método para enviar el correo
email_sender.send_email()