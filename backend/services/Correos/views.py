
import sys
import os
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, get_connection, send_mass_mail
from django.utils.html import strip_tags
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from database.models import ActiveLoan, Borrower

# Obtener cierta información para los recordatorios
def lista_pagos(request):
    pagos = ActiveLoan.objects.values('Amount', 'AmountToPay', 'borrower_id')  # Obtiene los registros de la tabla ActiveLoans
    return pagos

def usuarios_pagos(borrower_id):
    try:
        # Obtiene el objeto Borrower basado en el ID proporcionado
        borrower = Borrower.objects.get(id=borrower_id)

        # Recupera los datos 
        borrower_data = {
            'Name_borrower': borrower.Name_borrower, 
            'Email_borrower': borrower.Email_borrower,  
        }

        return borrower_data

    except Borrower.DoesNotExist:
        # Si el Borrower no existe, retorna un error
        return {'error': 'Usuario no encontrado'}
