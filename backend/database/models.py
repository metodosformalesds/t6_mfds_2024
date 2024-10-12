from django.db import models

# Create your models here.

#Borrower Model
class Borrower(models.model):
    id_borrower = models.CharField(primary_key=True) #Clave unica del usuario prestatario
    
    '''
    Agregar al finalizar modelo loan:
    loan = models.ForeignKey(Loans, on_delete=models.CASCADE)  #relacion con la entidad loan
    '''
    Username_borrower = models.CharField(max_length=50) #Nombre de usuario del prestatario
    Name_borrower = models.CharField() #Nombre completo del prestatario
    Firstname_borrower = models.CharField() #Primer nombre del prestatario
    Middlename_borrower = models.CharField() #Segundo nombre del prestatario
    Firstsurname_borrower = models.CharField() #Primer apellido o apellido paterno del prestatario
    Secondsurname_borrower = models.CharField() #Segundo apellido o apellido materno del prestatario
    Email_borrower = models.CharField() #Direccion de correo electronico del prestatario
    Password_borrower = models.CharField(max_length=60) #Contraseña de la cuenta del prestatario
    Phonenumber_borrower = models.IntegerField(max_length=10) #Numero de telefono del prestatario
    RFC_borrower = models.CharField(max_length=13) #Registro Federal de Contribuyentes (RFC) relacionado al prestatario
    Fulladdress_borrower = models.CharField() #Direccion completa del prestatario
    City_borrower = models.CharField() #Ciudad del prestatario
    neighboorn_borrower = models.CharField() #Vecindario, barrio, colonia o fraccionamiento del prestatario
    CP_borrower = models.IntegerField(max_length=5) #Codigo postal del prestatario
    State_borrower = models.CharField() #Estado del territorio o estado del prestatario
    Country_borrower = models.CharField() #Pais del prestatario
    PossibilityOfPay = models.FloatField(decimal_places=2) #número que indica la posibilidad de que el prestatario cumpla con los pagos
    ScoreLlamas = models.IntegerField() #Puntaje de calificación del prestatario dentro de la aplicación

#Moneylender Model
class Moneylender(models.model):
    id_moneylender = models.CharField(primary_key=True) #Clave unica del usuario prestamista 
    username_moneylender = models.CharField(max_length=50) #Nombre de usuario del prestamista
    Name_moneylender = models.CharField() #Nombre completo del prestamista
    Email_moneylender = models.CharField() #Direccion de correo electronico del prestamista
    Password_moneylender = models.CharField(max_length=60) #Contraseña de la cuenta del prestamista
    Subscription = models.BooleanField() #Estado que indica si el prestamista pago la suscripcion
    LoansActive = models.IntegerField() #Prestamos que el prestatario tiene publicados/activos

#Credit History Model
class CreditHistory(models.Model):
    id_check = models.AutoField(primary_key=True)  # Clave única
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)  # Relación con el prestatario
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

#Request model
class UserRequest(models.Model):
    id_request = models.AutoField(primary_key=True) #llave unica de la entidad
    Usercheck = models.ForeignKey(CreditHistory, on_delete=models.CASCADE) # llave foranea de la entidad CreditHistory,
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)  # Relación con el prestatario
    moneylender = models.ForeignKey(Moneylender, on_delate=models.CASCADE) #relacion con el prestamista
    
    #estos atributos aun no estan creados
    
    #loan = models.ForeignKey(Loans, on_delete=models.CASCADE)  #relacion con la entidad loan
