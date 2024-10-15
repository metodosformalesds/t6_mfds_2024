from django.db import models

#Moneylender Model
class Moneylender(models.Model):
    id_Moneylender = models.AutoField(primary_key=True, max_length=10) #Clave unica del usuario prestamista
    Username_Moneylender = models.CharField(max_length=50) #Nombre de usuario del prestatario
    Name_Moneylender = models.CharField(max_length=100) #Nombre completo del prestatario
    Firstname_Moneylender = models.CharField(max_length=50) #Primer nombre del prestatario
    Middlename_Moneylender = models.CharField(max_length=50) #Segundo nombre del prestatario
    Firstsurname_Moneylender = models.CharField(max_length=50) #Primer apellido o apellido paterno del prestatario
    Secondsurname_Moneylender = models.CharField(max_length=50) #Segundo apellido o apellido materno del prestatario
    BirthDate_Moneylender = models.CharField() #Fecha de nacimiento del prestamista
    Email_Moneylender = models.CharField(max_length=100) #Direccion de correo electronico del prestatario
    Password_Moneylender = models.CharField(max_length=60) #Contraseña de la cuenta del prestatario
    Phonenumber_Moneylender = models.CharField(max_length=10) #Numero de telefono del prestatario
    RFC_Moneylender = models.CharField(max_length=13) #Registro Federal de Contribuyentes (RFC) relacionado al prestatario
    CIEC_Moneylender = models.CharField(max_length=100) #Clave de Identificación Electrónica Confidencial del prestatario
    Fulladdress_Moneylender = models.CharField(max_length=200) #Direccion completa del prestatario
    City_Moneylender = models.CharField(max_length=50) #Ciudad del prestatario
    neighboorn_Moneylender = models.CharField(max_length=50) #Vecindario, barrio, colonia o fraccionamiento del prestatario
    CP_Moneylender = models.CharField(max_length=5) #Codigo postal del prestatario
    State_Moneylender = models.CharField(max_length=50) #Estado del territorio o estado del prestatario
    Country_Moneylender = models.CharField(max_length=50) #Pais del prestatario
    Subscription_Moneylender = models.BooleanField() #Valor que indica si el prestamista pago la suscripcion
    LoansActive_Moneylender = models.IntegerField() #Numero de prestamos que tiene activos el prestamista

#Invoice Model
class InvoiceHistory(models.Model):
    ID_invoice = models.AutoField(primary_key=True) #Clave unica del historial de facturas
    UUID = models.CharField(max_length=100) #UUID (Universally Unique Identifier), identificador asignado por el SAT a la factura
    Download_date = models.DateField() #Fecha de descarga de la factura
    CFDI_date = models.DateField() #Fecha de creacion de la factura
    Timbre_date = models.DateField() #Fecha del timbre del SAT que certifica la factura
    Cancellation_date = models.DateField(null=True) #Fecha de cancelacion de la factura en dado caso de haber sido cancelada
    Status_date = models.DateField() #Fecha de la ultima actualizacion del estatus
    Issuing_party = models.CharField(max_length=100) #Emisor de la factura
    Receiving_party = models.CharField(max_length=100) #Receptopr de la factura
    Type = models.CharField(max_length=100) #Tipo de factura
    Status = models.CharField(max_length=100) #Estatus de factura
    Total = models.DecimalField(max_digits=10, decimal_places=2) #Monto total de la factura
    Acuse = models.BooleanField() #Indicativo de la existencia de un acuse
    Invoice_pay = models.BooleanField() #Indicativo de si ya se pago la factura

#Loans Model
class Loans(models.Model):
    ID_Loan = models.AutoField(primary_key=True, max_length=10)
    ID_Moneylender = models.ForeignKey(Moneylender, on_delete=models.CASCADE)
    Amount = models.FloatField()
    Difficulty = models.IntegerField()
    InterestRate = models.FloatField()
    PaymentTerm = models.DateField()
    Amortization = models.DecimalField(max_digits=10, decimal_places=2)

#Borrower Model
class Borrower(models.Model):
    id_borrower = models.AutoField(primary_key=True, max_length=10) #Clave unica del usuario prestatario
    loan = models.ForeignKey(Loans, on_delete=models.CASCADE, null=True, blank= True)  #relacion con la entidad loan
    InvoiceHistory = models.ForeignKey(InvoiceHistory, on_delete=models.CASCADE) #Relacion con la tabla del historial de facturas
    Username_borrower = models.CharField(max_length=50) #Nombre de usuario del prestatario
    Name_borrower = models.CharField(max_length=100) #Nombre completo del prestatario
    Firstname_borrower = models.CharField(max_length=50) #Primer nombre del prestatario
    Middlename_borrower = models.CharField(max_length=50) #Segundo nombre del prestatario
    Firstsurname_borrower = models.CharField(max_length=50) #Primer apellido o apellido paterno del prestatario
    Secondsurname_borrower = models.CharField(max_length=50) #Segundo apellido o apellido materno del prestatario
    BirthDate_borrower = models.DateField() #Fecha de nacimiento del prestatario
    Email_borrower = models.CharField(max_length=100) #Direccion de correo electronico del prestatario
    Password_borrower = models.CharField(max_length=60) #Contraseña de la cuenta del prestatario
    Phonenumber_borrower = models.CharField(max_length=10) #Numero de telefono del prestatario
    RFC_borrower = models.CharField(max_length=13) #Registro Federal de Contribuyentes (RFC) relacionado al prestatario
    CIEC_borrower = models.CharField(max_length=100) #Clave de Identificación Electrónica Confidencial del prestatario
    Fulladdress_borrower = models.CharField(max_length=200) #Direccion completa del prestatario
    City_borrower = models.CharField(max_length=50) #Ciudad del prestatario
    neighboorn_borrower = models.CharField(max_length=50) #Vecindario, barrio, colonia o fraccionamiento del prestatario
    CP_borrower = models.CharField(max_length=5) #Codigo postal del prestatario
    State_borrower = models.CharField(max_length=50) #Estado del territorio o estado del prestatario
    Country_borrower = models.CharField(max_length=50) #Pais del prestatario
    PossibilityOfPay = models.DecimalField(max_digits=10, decimal_places=2) #número que indica la posibilidad de que el prestatario cumpla con los pagos
    ScoreLlamas = models.IntegerField() #Puntaje de calificación del prestatario dentro de la aplicación

#Credit History Model
class CreditHistory(models.Model):
    id_check = models.AutoField(primary_key=True, max_length=20)  # Clave única
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
    Borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)  # Relación con el prestatario
    moneylender = models.ForeignKey(Moneylender, on_delete=models.CASCADE) #relacion con el prestamista
    
class LoanDetails(models.Model):
    ID_LoanActive = models.IntegerField(primary_key=True)
    ID_Loan = models.ForeignKey(Loans, on_delete=models.CASCADE)
    ID_Moneylender = models.ForeignKey(Moneylender, on_delete=models.CASCADE)
    ID_Borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    Totaldebt = models.DecimalField(max_digits=10, decimal_places=2)
    TotaldebtPay = models.DecimalField(max_digits=10, decimal_places=2)
    AmountToPay = models.DecimalField(max_digits=10, decimal_places=2)
    DayOfPay = models.DateField()
    PastDueBalance = models.DecimalField(max_digits=10, decimal_places=2)

