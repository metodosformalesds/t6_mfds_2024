from django.db import models

#Moneylender Model
class Moneylender(models.Model):
    id_moneylender = models.AutoField(primary_key=True) #Clave unica del usuario prestamista 
    username_moneylender = models.CharField(max_length=50) #Nombre de usuario del prestamista
    Name_moneylender = models.CharField(max_length=50) #Nombre completo del prestamista
    Email_moneylender = models.CharField(max_length=100) #Direccion de correo electronico del prestamista
    Password_moneylender = models.CharField(max_length=60) #Contraseña de la cuenta del prestamista
    Subscription = models.BooleanField() #Estado que indica si el prestamista pago la suscripcion
    LoansActive = models.IntegerField() #Prestamos que el prestatario tiene publicados/activos

#Loans Model
class Loans(models.Model):
    ID_Loan = models.AutoField(primary_key=True)
    ID_Moneylender = models.ForeignKey(Moneylender, on_delete=models.CASCADE)
    Amount = models.FloatField()
    Difficulty = models.IntegerField()
    InterestRate = models.FloatField()
    PaymentTerm = models.DateField()
    Amortization = models.DecimalField(max_digits=10, decimal_places=2)



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


#Borrower Model
class Borrower(models.Model):
    id_borrower = models.AutoField(primary_key=True) #Clave unica del usuario prestatario
    loan = models.ForeignKey(Loans, on_delete=models.CASCADE, null=True, blank= True)  #relacion con la entidad loan
    invoice_history = models.ForeignKey(InvoiceHistory, on_delete=models.CASCADE) #Relacion con la tabla del historial de facturas
    Username_borrower = models.CharField(max_length=50) #Nombre de usuario del prestatario
    Name_borrower = models.CharField(max_length=100) #Nombre completo del prestatario
    Firstname_borrower = models.CharField(max_length=50) #Primer nombre del prestatario
    Middlename_borrower = models.CharField(max_length=50) #Segundo nombre del prestatario
    Firstsurname_borrower = models.CharField(max_length=50) #Primer apellido o apellido paterno del prestatario
    Secondsurname_borrower = models.CharField(max_length=50) #Segundo apellido o apellido materno del prestatario
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
    PossibilityOfPay = models.FloatField() #número que indica la posibilidad de que el prestatario cumpla con los pagos
    ScoreLlamas = models.IntegerField() #Puntaje de calificación del prestatario dentro de la aplicación

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
    Borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)  # Relación con el prestatario
    moneylender = models.ForeignKey(Moneylender, on_delete=models.CASCADE) #relacion con el prestamista
    
class ActiveLoans(models.Model):
    IDLoanActive = models.AutoField(primary_key=True)  # ID único del préstamo activo
    loan = models.ForeignKey('Loans', on_delete=models.CASCADE)  # Relación con el modelo Loans
    borrower = models.ForeignKey('Borrower', on_delete=models.CASCADE)  # Relación con el modelo Borrower (quien recibe el dinero)
    moneylender = models.ForeignKey('Moneylender', on_delete=models.CASCADE)  # Relación con el modelo Moneylender (quien presta el dinero)

    TotalDebt = models.DecimalField(max_digits=10, decimal_places=2)  # Cantidad total de la deuda
    TotalDebtPay = models.DecimalField(max_digits=10, decimal_places=2)  # Cantidad pagada por el prestatario
    AmountToPay = models.DecimalField(max_digits=10, decimal_places=2)  # Cantidad que debe pagar el prestatario
    DayOfPay = models.DateField()  # Fecha de pago actual
    PastDueBalance = models.DecimalField(max_digits=10, decimal_places=2)  # Saldo vencido

    def __str__(self):
        return f"Loan {self.loan} Active - Borrower: {self.borrower} - Moneylender: {self.moneylender}"

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('payment', 'Payment'),
        ('payout', 'Payout'),
    ]

    ID_Transaction = models.AutoField(primary_key=True)
    ID_ActiveLoan = models.ForeignKey(ActiveLoans, on_delete=models.CASCADE)
    AmountPaid = models.FloatField()
    PaymentDate = models.DateTimeField(auto_now_add=True)
    PayPalTransactionID = models.CharField(max_length=100, unique=True)
    Status = models.CharField(max_length=20, choices=[('completed', 'Completed'), ('failed', 'Failed'), ('pending', 'Pending')])
    TransactionType = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)

