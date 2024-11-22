# correos/email_sender.py
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
"""
Recibe los datos para realizar el envío de correo electronico.

        Parámetros:
            recipien: Recibe el correo que recibirá el mensaje
            Subject:  Recibe el asunto del mensaje
            Template_name: Recibe la plantilla que se va a utilizar
            Context: Brinda los parametros adicioanles que se usarán en la plantilla

        Proceso:
            - Utiliza el proceso de send_mail para poder enviar el correo y en caso falle el envío  brindar un mensaje de error.
        Retorna:    
            Un mensaje en consola de que el mensaje se envió de forma exitosa.
"""
class EmailSender:
    def __init__(self, recipient, subject, template_name, context = None):
        self.recipient = recipient
        self.subject = subject
        self.template_name = template_name  # Nombre del archivo HTML en templates
        self.context = context or {} # Contexto para la plantilla
    
    def send_email(self):
        try:
 
            html_message = render_to_string(self.template_name, self.context)
            

            send_mail(
                subject=self.subject,
                message="",  
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.recipient],
                html_message=html_message,  
                fail_silently=False,
            )
            print("Correo enviado con éxito")
            #envía los datos y la plantilla al correo del usuario
        except Exception as e:
            print(f"Error al enviar el correo: {e}")