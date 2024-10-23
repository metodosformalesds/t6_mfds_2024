from django.db import models

#Moneylender Model

class Moneylender(models.Model):
    id = models.AutoField(primary_key=True)  # Clave única del prestamista
    username = models.CharField(max_length=50)  # Nombre de usuario del prestamista
    full_name = models.CharField(max_length=100)  # Nombre completo del prestamista
    first_name = models.CharField(max_length=50)  # Primer nombre
    middle_name = models.CharField(max_length=50, blank=True, null=True)  # Segundo nombre (opcional)
    first_surname = models.CharField(max_length=50)  # Primer apellido
    second_surname = models.CharField(max_length=50, blank=True, null=True)  # Segundo apellido (opcional)
    birth_date = models.DateField()  # Fecha de nacimiento
    email = models.EmailField(max_length=100, unique=True)  # Dirección de correo electrónico
    password = models.CharField(max_length=60)  # Contraseña 
    phone_number = models.CharField(max_length=15)  # Número de teléfono  
    rfc = models.CharField(max_length=13, unique=True)  # Registro Federal de Contribuyentes
    ciec = models.CharField(max_length=100)  # Clave de Identificación Electrónica Confidencial
    full_address = models.CharField(max_length=200)  # Dirección completa
    city = models.CharField(max_length=50)  # Ciudad
    neighborhood = models.CharField(max_length=50)  # Vecindario, barrio o colonia
    postal_code = models.CharField(max_length=5)  # Código postal
    state = models.CharField(max_length=50)  # Estado
    country = models.CharField(max_length=50)  # País
    is_subscribed = models.BooleanField(default=False)  # Indica si pagó la suscripción
    active_loans = models.PositiveIntegerField(default=0)  # Número de préstamos activos

#Loans Model
class Loan(models.Model):
    id = models.AutoField(primary_key=True)  # ID único del préstamo
    moneylender = models.ForeignKey(Moneylender, on_delete=models.CASCADE)  # Relación con el modelo Moneylender
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Monto del préstamo
    difficulty = models.IntegerField()  # Dificultad del préstamo
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Tasa de interés del préstamo
    payment_term = models.DateField()  # Plazo de pago del préstamo
    amortization = models.DecimalField(max_digits=10, decimal_places=2)  # Monto de amortización


class InvoiceHistory(models.Model):
    id = models.AutoField(primary_key=True)  # Clave única del historial de facturas
    uuid = models.CharField(max_length=100)  # UUID (Universally Unique Identifier), identificador asignado por el SAT a la factura
    download_date = models.DateField()  # Fecha de descarga de la factura
    cfdi_date = models.DateField()  # Fecha de creación de la factura
    timbre_date = models.DateField()  # Fecha del timbre del SAT que certifica la factura
    cancellation_date = models.DateField(null=True)  # Fecha de cancelación de la factura en dado caso de haber sido cancelada
    status_date = models.DateField()  # Fecha de la última actualización del estatus
    issuing_party = models.CharField(max_length=100)  # Emisor de la factura
    receiving_party = models.CharField(max_length=100)  # Receptor de la factura
    type = models.CharField(max_length=100)  # Tipo de factura
    status = models.CharField(max_length=100)  # Estatus de factura
    total = models.DecimalField(max_digits=10, decimal_places=2)  # Monto total de la factura
    acuse = models.BooleanField()  # Indicativo de la existencia de un acuse
    invoice_pay = models.BooleanField()  # Indicativo de si ya se pagó la factura

#Borrower Model

class Borrower(models.Model):
    id = models.AutoField(primary_key=True)  # Clave única del usuario prestatario
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, null=True, blank=True)  # Relación con la entidad loan
    invoice_history = models.ForeignKey(InvoiceHistory, on_delete=models.CASCADE)  # Relación con la tabla del historial de facturas
    username = models.CharField(max_length=50)  # Nombre de usuario del prestatario
    name = models.CharField(max_length=100)  # Nombre completo del prestatario
    first_name = models.CharField(max_length=50)  # Primer nombre del prestatario
    middle_name = models.CharField(max_length=50)  # Segundo nombre del prestatario
    first_surname = models.CharField(max_length=50)  # Primer apellido o apellido paterno del prestatario
    second_surname = models.CharField(max_length=50)  # Segundo apellido o apellido materno del prestatario
    birth_date = models.DateField()  # Fecha de nacimiento del prestatario
    email = models.CharField(max_length=100)  # Dirección de correo electrónico del prestatario
    password = models.CharField(max_length=60)  # Contraseña de la cuenta del prestatario
    phone_number = models.CharField(max_length=10)  # Número de teléfono del prestatario
    rfc = models.CharField(max_length=13)  # Registro Federal de Contribuyentes (RFC) relacionado al prestatario
    ciec = models.CharField(max_length=100)  # Clave de Identificación Electrónica Confidencial del prestatario
    full_address = models.CharField(max_length=200)  # Dirección completa del prestatario
    city = models.CharField(max_length=50)  # Ciudad del prestatario
    neighborhood = models.CharField(max_length=50)  # Vecindario, barrio, colonia o fraccionamiento del prestatario
    cp = models.CharField(max_length=5)  # Código postal del prestatario
    state = models.CharField(max_length=50)  # Estado del territorio o estado del prestatario
    country = models.CharField(max_length=50)  # País del prestatario
    possibility_of_pay = models.FloatField()  # Número que indica la posibilidad de que el prestatario cumpla con los pagos
    score_llamas = models.IntegerField()  # Puntaje de calificación del prestatario dentro de la aplicación

#Credit History Model
class CreditHistory(models.Model):
    id = models.AutoField(primary_key=True)  # Clave única 
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)  # Relación con el prestatario
    date_account_open = models.DateField()          # Fecha de apertura de la cuenta
    actual_balance = models.DecimalField(max_digits=10, decimal_places=2)  # 
    max_credit = models.DecimalField(max_digits=10, decimal_places=2)  #
    lim_credit = models.DecimalField(max_digits=10, decimal_places=2)  #
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
    salary = models.FloatField() # Salario

#Request model
class Request(models.Model):
    id= models.AutoField(primary_key=True) #llave unica de la entidad
    credit_history = models.ForeignKey(CreditHistory, on_delete=models.CASCADE) # llave foranea de la entidad CreditHistory,
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)  # Relación con el prestatario
    moneylender = models.ForeignKey(Moneylender, on_delete=models.CASCADE) #relacion con el prestamista
    
class ActiveLoan(models.Model):
    id = models.AutoField(primary_key=True)  # ID único del préstamo activo
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)  # Relación con el modelo Loans
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)  # Relación con el modelo Borrower (quien recibe el dinero)
    moneylender = models.ForeignKey(Moneylender, on_delete=models.CASCADE)  # Relación con el modelo Moneylender (quien presta el dinero)
    total_debt = models.DecimalField(max_digits=10, decimal_places=2)  # Cantidad total de la deuda
    total_debt_paid = models.DecimalField(max_digits=10, decimal_places=2)  # Cantidad pagada por el prestatario
    amount_to_pay = models.DecimalField(max_digits=10, decimal_places=2)  # Cantidad que debe pagar el prestatario
    day_of_pay = models.DateField()  # Fecha de pago actual
    past_due_balance = models.DecimalField(max_digits=10, decimal_places=2)  # Saldo vencido

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('payment', 'Payment'),
        ('payout', 'Payout'),
    ]

    id = models.AutoField(primary_key=True)  # ID único de la transacción
    active_loan = models.ForeignKey(ActiveLoan, on_delete=models.CASCADE)  # Relación con el modelo ActiveLoan
    amount_paid = models.FloatField()  # Monto pagado en la transacción
    payment_date = models.DateTimeField(auto_now_add=True)  # Fecha de pago (se agrega automáticamente)
    paypal_transaction_id = models.CharField(max_length=100, unique=True)  # ID de la transacción de PayPal (único)
    status = models.CharField(max_length=20, choices=[('completed', 'Completed'), ('failed', 'Failed'), ('pending', 'Pending')])  # Estado de la transacción
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)  # Tipo de transacción
