from django.db import models

# Create your models here.






#Credit History Model
class CreditHistory(models.Model):
    id_check = models.AutoField(primary_key=True)  # Clave única
    
    #Agregar cuando se complete el modelo de Borrower
    #borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)  # Relación con el prestatario
    
    date_account_open = models.DateField()          # Fecha de apertura de la cuenta
    actual_balance = models.DecimalField(max_digits=10, decimal_places=2)  # Saldo pendiente
    max_credit = models.DecimalField(max_digits=10, decimal_places=2)      # Cantidad máxima solicitada
    lim_credit = models.DecimalField(max_digits=10, decimal_places=2)       # Monto máximo disponible
    pay_history = models.CharField(max_length=50)  # Historial de pagos
    current_pay_status = models.CharField(max_length=10)  # Estado actual de los pagos
    accounts_open = models.IntegerField()           # Cuentas activas
    accounts_closed = models.IntegerField()         # Cuentas cerradas
    account_fixed_payment = models.BooleanField()   # Cuentas con pago fijo
    num_mop1 = models.IntegerField()                # Pagos a tiempo
    num_mop2 = models.IntegerField()                # Retrasos de 1 a 29 días
    num_mop3 = models.IntegerField()                # Retrasos de 30 a 59 días
    num_mop4 = models.IntegerField()                # Retrasos de 60 a 89 días
    num_mop5 = models.IntegerField()                # Retrasos de 90 a 119 días
    num_mop6 = models.IntegerField()                # Retrasos de 120 a 149 días
    num_mop7 = models.IntegerField()                # Retrasos de 150 a 179 días
    check_date = models.DateField()                 # Fecha de consulta
    code_score = models.FloatField()              # Score crediticio
    place_of_work = models.CharField(max_length=100)  # Lugar de trabajo
    salary = models.DecimalField(max_digits=10, decimal_places=2)  # Salario


class Request(models.Model):
    id_request = models.AutoField(primary_key=True) #llave unica de la entidad
    check = models.ForeignKey(CreditHistory, on_delete=models.CASCADE) # llave foranea de la entidad CreditHistory,

    #estos atributos aun no estan creados
    
    #loan = models.ForeignKey(Loans, on_delete=models.CASCADE)  #relacion con la entidad loan
    #borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)  # Relación con el prestatario
    #moneylender = models.ForeignKey(moneylender, on_delate=models.CASCADE) #relacion con el prestamista
