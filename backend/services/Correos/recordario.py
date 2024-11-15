# recordatorio.py
from django.utils import timezone
from views import lista_pagos, usuarios_pagos  # Importa la función desde views
from datetime import datetime, timedelta
from send_mail import EmailSender

def check_active_loan_dates():
    fecha_hace_5_dias = datetime.now() - timedelta(days=5)  
    pagos = lista_pagos()  # Llama a la función para obtener los pagos

    # Itera sobre los pagos obtenidos
    for pago in pagos:
        if pago['AmountToPay'] < fecha_hace_5_dias:  # Compara con la fecha de hace 5 días
          
          
            usuario = usuarios_pagos(pago['borrower_id'])  # Llama a usuarios_pagos pasándole el ID

            if usuario and 'Email_borrower' in usuario:  # Asegura que el usuario existe y tiene correo
                email_sender = EmailSender(
                    recipient=usuario['Email_borrower'],  # Aquí usas la variable correctamente
                    subject='Tu fecha de pago está cerca',
                    template_name='envio.html',
                    context={
                        'nombre': usuario['Name_borrower']  # Contexto que va a la plantilla
                    }
                )
                email_sender.send_email()
            else:
                print(f"No se encontró al usuario con ID {pago['borrower_id']}")
