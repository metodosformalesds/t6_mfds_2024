import sqlite3
from datetime import datetime, timedelta
from send_mail import EmailSender
import os
import sys
import django
"""
Envia recordatorios de pago 5 días antes a los usuarios que aun no hayan realizado el pago de su prestamo
        Parámetros:
            recipien: Recibe el correo que recibirá el mensaje
            Subject:  Recibe el asunto del mensaje
            Template_name: Recibe la plantilla que se va a utilizar
            Context: Brinda los parametros adicioanles que se usarán en la plantilla

        Proceso:
            - Se ejecuta mediante github actions o consola para realizar pruebas, esre recibe la fecha de pago y despues si esta es iguala  5 dias antes de pago
              envía busca el correo y nombre del usuario. Despues, envia la plantilla de recordatorio de pago
        Retorna:    
            Un mensaje en consola de que el mensaje se envió de forma exitosa.
"""
# Obtén la ruta absoluta del directorio raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'llamascoin.settings')
django.setup()

DB_PATH = '../../db.sqlite3'

def lista_pagos():
    conn = None
    try:
        print("Intentando conectarse a la base de datos...")
        conn = sqlite3.connect(DB_PATH)
        print("Conexión a la base de datos exitosa.")
        cursor = conn.cursor()
        # Consulta para obtener los pagos
        print("Ejecutando consulta para obtener pagos...")
        cursor.execute("SELECT DayOfPay, borrower_id FROM database_activeloans WHERE DATE(DayOfPay) = DATE('now', '+5 days')")
        pagos = cursor.fetchall()
        """Obtiene los datos y los almacena en tuplas de forma temporal"""
        if not pagos:
            print("No se encontraron pagos con la fecha solicitada.")

        # Convierte los resultados en una lista de diccionarios
        
        columns = [desc[0] for desc in cursor.description]
        """Obtiene los datos que se almacenaron y los devuelve en una lista"""
        resultados = [dict(zip(columns, row)) for row in pagos]
        """Obtiene los resultados y los convierte en una lista de diccionario"""
        return resultados
    
    except sqlite3.Error as e:
        # Manejo de errores en caso de fallos de conexión
        print(f"Error al conectar a la base de datos: {e}")
        return []
    
    finally:
        # Cierra la conexión si está abierta
        if conn:
            conn.close()
            print("Conexión cerrada.")

def usuarios_pagos(borrower_id):
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Consulta para obtener el usuario por borrower_id
        cursor.execute("SELECT Email_borrower,Name_borrower FROM database_borrower WHERE id_borrower = ?", (borrower_id,))
        usuario = cursor.fetchone()
        """Obtiene la primera fila del resultado y los almacena en una dupla"""
        if usuario:
            print(f"Usuario encontrado: {usuario}")
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, usuario))
            """retorna un diccionario de los datos en columnas"""
        else:
            print(f"No se encontró usuario con borrower_id {borrower_id}")
        return None
    except sqlite3.Error as e:
        print(f"Error al consultar el usuario con borrower_id {borrower_id}: {e}")
        return None
    finally:
        if conn:
            conn.close()

def check_active_loan_dates():
    print("Iniciando verificación de pagos...")
    pagos = lista_pagos()

    if not pagos:
        print("No se encontraron pagos con fecha 5 días antes de la fecha actual.")
        return

    for pago in pagos:
        print(f"Procesando borrower_id: {pago['borrower_id']}")
        usuario = usuarios_pagos(pago['borrower_id'])

        if usuario and 'Email_borrower' in usuario:
            print(f"Enviando correo a: {usuario['Email_borrower']}")
            email_sender = EmailSender(
                recipient=usuario['Email_borrower'],
                subject='Tu fecha de pago está cerca',
                template_name='envio.html',
                context={
                    'nombre': usuario['Name_borrower']
                }
            )
            email_sender.send_email()
            """Envia los datos obtenidos, la plantilla y los daots originales a email_sender para enviar el correo"""
        else:
            print(f"No se encontró al usuario con ID {pago['borrower_id']}.")


if __name__ == "__main__":
    check_active_loan_dates()
