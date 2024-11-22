# correos/email_sender.py
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

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
                html_message=html_message,  # Cuerpo en HTML
                fail_silently=False,
            )
            print("Correo enviado con éxito")
            """envía los datos y la plantilla al correo del usuario"""
        except Exception as e:
            print(f"Error al enviar el correo: {e}")