from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser

#Modelo de usuario personalizado
class User(AbstractBaseUser):
    """
    Modelo personalizado de usuario que extiende `AbstractBaseUser` para incluir campos específicos
    como correo electrónico, CURP, tipo de cuenta, y estado de verificación.

    Este modelo utiliza el correo electrónico como identificador único (`USERNAME_FIELD`) en lugar
    del nombre de usuario estándar. Incluye un conjunto de campos requeridos que deben proporcionarse
    al crear un usuario.

    Campos:
        email (EmailField): Dirección de correo electrónico única utilizada como identificador principal.
        paypal_email (EmailField): Correo electrónico asociado a PayPal (opcional).
        curp (CharField): Clave Única de Registro de Población (CURP), única por usuario.
        account_type (CharField): Tipo de cuenta del usuario (por ejemplo, prestatario o prestamista).
        is_verified (BooleanField): Indica si el usuario ha sido verificado en el sistema.

    Atributos adicionales:
        USERNAME_FIELD (str): Campo utilizado para la autenticación. En este caso, es "email".
        REQUIRED_FIELDS (list): Lista de campos adicionales requeridos al crear un usuario
                                (excluyendo el campo `USERNAME_FIELD` y la contraseña).
    """
    email = models.EmailField(("Direccion de correo"), max_length=254,unique=True)
    paypal_email = models.EmailField(blank=True)
    curp = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(max_length=20)
    is_verified = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("paypal_email","curp", "account_type")
    
class Moneylender(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #Vincular a un usuario token de DRF
    first_name = models.CharField(max_length=50)  # Primer nombre
    middle_name = models.CharField(max_length=50, blank=True, null=True)  # Segundo nombre (opcional)
    first_surname = models.CharField(max_length=50)  # Primer apellido
    second_surname = models.CharField(max_length=50, blank=True, null=True)  # Segundo apellido (opcional)
    birth_date = models.CharField(max_length=20)   # Fecha de nacimiento
    phone_number = models.CharField(max_length=15)  # Número de teléfono  
    rfc = models.CharField(max_length=13, unique=True)  # Registro Federal de Contribuyentes
    full_address = models.CharField(max_length=200)  # Dirección completa
    city = models.CharField(max_length=50)  # Ciudad
    neighborhood = models.CharField(max_length=50)  # Vecindario, barrio o colonia
    postal_code = models.CharField(max_length=5)  # Código postal
    state = models.CharField(max_length=50)  # Estado
    country = models.CharField(max_length=50)  # País
    municipality = models.CharField(max_length=50, blank=True)
    nationality = models.CharField(max_length=50, default= 'MX') 

    is_subscribed = models.BooleanField(default=False)  # Indica si pagó la suscripción
    active_loans = models.PositiveIntegerField(default=0)  # Número de préstamos activos

#Loans Model
class Loan(models.Model):
    TERM_CHOICES = [ #Eleccion de plazos
        (1, 'Semanal'),    
        (2, 'Quincenal'),  
        (3, 'Mensual'),   
    ]
    id = models.AutoField(primary_key=True)  # ID único del préstamo
    moneylender = models.ForeignKey(Moneylender, related_name='loans', on_delete=models.CASCADE)  # Relación con el modelo Moneylender
    amount = models.DecimalField(max_digits=10, decimal_places=2)# Monto total del préstamo
    total_amount= models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True) # Monto total con intereses
    difficulty = models.IntegerField()  # Dificultad del préstamo
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Tasa de interés del préstamo
    number_of_payments = models.IntegerField(default=12)  # Número de pagos
    term = models.IntegerField(choices=TERM_CHOICES, default=3)  # Plazo del préstamo (semanal, quincenal, mensual)
    publication_date = models.DateField(default=timezone.now)  # Fecha de publicación del préstamo
    payment_per_term = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Pago periodico
    duration_loan = models.CharField(max_length=50, blank=True, null=True) #Duracion de prestamo expresado en meses y dias

class Borrower(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #Vincular a un usuario token de DRF
    first_name = models.CharField(max_length=50)  # Primer nombre del prestatario
    middle_name = models.CharField(max_length=50, blank=True, null=True)   # Segundo nombre del prestatario
    first_surname = models.CharField(max_length=50)  # Primer apellido o apellido paterno del prestatario
    second_surname = models.CharField(max_length=50)  # Segundo apellido o apellido materno del prestatario
    birth_date = models.CharField(max_length=50)   # Fecha de nacimiento del prestatario
    phone_number = models.CharField(max_length=10)  # Número de teléfono del prestatario
    rfc = models.CharField(max_length=13)# Registro Federal de Contribuyentes (RFC) relacionado al prestatario
    full_address = models.CharField(max_length=200)  # Dirección completa del prestatario
    city = models.CharField(max_length=50)  # Ciudad del prestatario
    neighborhood = models.CharField(max_length=50)  # Vecindario, barrio, colonia o fraccionamiento del prestatario
    postal_code = models.CharField(max_length=5)  # Código postal del prestatario
    state = models.CharField(max_length=50)  # Estado del territorio o estado del prestatario
    country = models.CharField(max_length=50)  # País del prestatario
    municipality = models.CharField(max_length=50, blank=True) #Municipio
    nationality = models.CharField(max_length=50, default= 'MX') #Nacionalidad
    
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
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE, related_name='invoices')


class CreditHistory(models.Model):
    """
    Modelo que representa el historial crediticio de un prestatario, combinando datos obtenidos
    del buró de crédito con información generada en la plataforma.

    Este modelo guarda información clave sobre el comportamiento de pagos del prestatario,
    estadísticas de sus préstamos y pagos, y métricas calculadas como el crédito disponible
    y la probabilidad de pago a tiempo.

    Campos:
        id (AutoField): Clave primaria única.
        borrower (ForeignKey): Relación con el prestatario asociado.
        date_account_open (DateField): Fecha de apertura de la cuenta del prestatario.
        
        # Datos del buró de crédito
        accounts_open (IntegerField): Total de cuentas abiertas registradas en el buró.
        accounts_closed (IntegerField): Total de cuentas cerradas.
        negative_accounts (IntegerField): Número de cuentas con comportamiento negativo.
        num_mopX (IntegerField): Número de cuentas por tipo de retraso (donde X = 1, 2, ..., 99).
        code_score (IntegerField): Código del modelo estadístico del buró.
        val_score (IntegerField): Valor del score calculado por el buró.
        check_date (DateField): Fecha de consulta al buró.

        # Datos generados en la plataforma
        credit_line (DecimalField): Línea de crédito asignada por la plataforma.
        score_llamas (IntegerField): Puntaje crediticio asignado dentro de la plataforma.
        on_time_payments (IntegerField): Cantidad de pagos realizados a tiempo.
        late_payments (IntegerField): Cantidad de pagos realizados fuera de tiempo.
        late_payments_over_week (IntegerField): Cantidad de pagos atrasados más de 7 días.
        on_time_payment_probability (DecimalField): Probabilidad estimada de pagar a tiempo.
        closed_loans (IntegerField): Cantidad de préstamos cerrados.
        active_loans (IntegerField): Cantidad de préstamos activos.
        available_credit (DecimalField): Crédito disponible para el prestatario.
        outstanding_balance (DecimalField): Saldo total pendiente de los préstamos activos.

    Métodos:
        calculate_llamas_history:
            Calcula y actualiza las estadísticas del historial de crédito, incluyendo:
            - Pagos a tiempo y tardíos.
            - Probabilidad de pago a tiempo.
            - Créditos cerrados y activos.
            - Línea de crédito disponible y saldo pendiente.

        adjust_credit_line:
            Ajusta la línea de crédito del prestatario en función de su `score_llamas`.

        adjust_llamas_score:
            Incrementa el `score_llamas` del prestatario basado en la dificultad del préstamo
            y si el pago fue realizado a tiempo.
    """
    id = models.AutoField(primary_key=True)  # Clave única 
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE,related_name='credit_history' )  # Relación con el prestatario
    date_account_open = models.DateField()  # Fecha de apertura de la cuenta
    
    #Datos consultados en el buro de credito
    accounts_open = models.IntegerField()           # “NumeroCuentas” : Presenta la suma total de los créditos integrados en el expediente del Cliente.
    accounts_closed = models.IntegerField()         # “CuentasCerradas”: Presenta la suma total de los créditos con fecha de cierre integrados en el expediente del Cliente.
    negative_accounts = models.IntegerField ()         # “CuentasNegativasActuales”: Presenta la suma total de créditos con MOP reportado igual o superior a 02.
    num_mop1 = models.IntegerField()                # Pagos a tiempo
    num_mop2 = models.IntegerField()                # suma total de créditos Retrasos de 1 a 29 días
    num_mop3 = models.IntegerField()                # suma total de créditos Retrasos de 30 a 59 días
    num_mop4 = models.IntegerField()                # suma total de créditos Retrasos de 60 a 89 días
    num_mop5 = models.IntegerField()                # suma total de créditos Retrasos de 90 a 119 días
    num_mop6 = models.IntegerField()                # suma total de créditos Retrasos de 120 a 149 días
    num_mop7 = models.IntegerField()                # suma total de créditos Retrasos de 150 a 179 días
    num_mop99 = models.IntegerField()               # Suma de cuentas reportadas por fraude 
    code_score = models.IntegerField()              # Presenta el código del modelo estadístico solicitado
    val_score = models.IntegerField(default=0)      # Presenta el valor del Score calculado o el valor de la estimación solicitada.
    check_date = models.DateField()                 # Fecha de consulta
    
    #Datos generados con el historial del Presstatario en la plataforma
    credit_line = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00) #Linea de cedito otorgada por LLamascoin
    score_llamas = models.IntegerField(default=1000)  # Puntaje de calificación del prestatario dentro de la aplicación
    on_time_payments = models.IntegerField(default=0) #Pagos a tiempo
    late_payments = models.IntegerField(default=0)    #Pagos tardios
    late_payments_over_week = models.IntegerField(default=0)  # Pagos atrasados por más de 7 días
    
    on_time_payment_probability = models.DecimalField(max_digits=5, decimal_places=2, default=0.0) #Probabilidad de que pague a tiempo
    
    closed_loans = models.IntegerField(default=0) #Prestamos cerrados
    active_loans = models.IntegerField(default=0) #Prestamos Activos
    available_credit = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) #Linea de credito disponible
    outstanding_balance = models.DecimalField(max_digits=10, decimal_places=2,default=0.0) #Saldo pendiente de pagar 
    
    def calculate_llamas_history(self):
        """
            Calcula y actualiza las estadísticas del historial de crédito, incluyendo:
            - Pagos a tiempo y tardíos.
            - Probabilidad de pago a tiempo.
            - Créditos cerrados y activos.
            - Línea de crédito disponible y saldo pendiente.
        """
        payments = Payments.objects.filter(active_loan__borrower=self.borrower)
        on_time_count = payments.filter(paid=True, paid_on_time=True).count()
        late_count = payments.filter(paid=True, paid_on_time=False).count()
        #Conteo de pagos
        self.on_time_payments = on_time_count
        self.late_payments = late_count
        
        # Calcular pagos atrasados por más de 7 días
        seven_days_ago = timezone.now() - timedelta(days=7)
        late_over_week_count = payments.filter(
            paid=False, 
            date_to_pay__lt=seven_days_ago
        ).count()
        
        # Calcular probabilidad de pago a tiempo
        total_payments = on_time_count + late_count
        self.on_time_payment_probability = (on_time_count / total_payments) * 100 if total_payments > 0 else 0.0

        # Calcular préstamos cerrados y activos
        self.closed_loans = ActiveLoan.objects.filter(borrower=self.borrower, amount_to_pay=0).count()
        self.active_loans = ActiveLoan.objects.filter(borrower=self.borrower).exclude(amount_to_pay=0).count()
        
        # Calcular el crédito disponible
        active_loans_debt = ActiveLoan.objects.filter(borrower=self.borrower).aggregate(total_debt=models.Sum('amount_to_pay'))['total_debt'] or 0
        self.available_credit = self.credit_line - active_loans_debt
        
        self.outstanding_balance = active_loans_debt
        self.on_time_payments = on_time_count
        self.late_payments = late_count
        self.late_payments_over_week = late_over_week_count
         
        self.save()
        self.adjust_credit_line()
    
    def adjust_credit_line(self):
        """
        Ajusta la línea de crédito del prestatario según su `score_llamas`.
        """
        if self.score_llamas >= 2750:
          self.credit_line = 15000
        elif self.score_llamas >= 2500:
          self.credit_line = 10000
        elif self.score_llamas >= 2250:
            self.credit_line = 7500
        elif self.score_llamas >= 1750:
            self.credit_line = 5500
        elif self.score_llamas >= 1500:
            self.credit_line = 3500
        elif self.score_llamas >= 1200:
            self.credit_line = 1500
        else:
           self.credit_line = 1000  # Línea de crédito base por defecto

        self.save()
        
    def adjust_llamas_score(self, loan, paid_on_time):
        """
        Ajusta el `score_llamas` del prestatario en función de la dificultad del préstamo y si el pago fue a tiempo.

        Parámetros:
            loan (Loan): Préstamo asociado al pago.
            paid_on_time (bool): Indica si el pago fue realizado a tiempo.
        """
        if not paid_on_time:
            return  # No se recompensa el llamascore si el pago no fue a tiempo
    # Calcular la dificultad del préstamo usando la función existente
        dificultad = self.difficulty
    # Establecer un índice de dificultad favorable
    # Mayor dificultad genera más incremento
        if dificultad < 30:
            incremento = 5
        elif dificultad < 50:
            incremento = 10
        elif dificultad < 70:
            incremento = 15
        elif dificultad < 90:
            incremento = 20
        else:
            incremento = 25
    # Incrementar el llamascore
        self.score_llamas += incremento
    # Asegurarse de que el llamascore no exceda un límite (por ejemplo, 3000)
        self.score_llamas = min(self.score_llamas, 3000)
    # Guardar los cambios en el historial de crédito
        self.save()
    
#Request model
class Request(models.Model):
    id = models.AutoField(primary_key=True)  # Llave única de la entidad
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE, related_name='requests')  # Relación con el prestatario
    moneylender = models.ForeignKey(Moneylender, on_delete=models.CASCADE, related_name='moneylender_requests')  # Relación con el prestamista
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='loan_requests')  # Relación con el préstamo que se solicitó
    STATUS_CHOICES = [
        ('pending', 'Pending'),  # Pendiente
        ('approved', 'Approved'),  # Aprobado
        ('rejected', 'Rejected'),  # Rechazado
        ('completed', 'Completed'),  # Completado
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # Estado de la solicitud
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación del registro

class ActiveLoan(models.Model):
    """
    Modelo que representa un préstamo activo dentro del sistema.

    Este registro se genera automáticamente cuando un prestamista aprueba 
    una solicitud de préstamo (Request). Contiene la información necesaria 
    para rastrear el estado y el progreso del préstamo, incluyendo al prestatario, 
    el prestamista, y los montos relacionados con la deuda.
    Atributos:
        id (int): ID único del préstamo activo.
        loan (ForeignKey): Relación con el modelo `Loan` que representa el préstamo aprobado.
        borrower (ForeignKey): Relación con el prestatario (`Borrower`) que recibe el préstamo.
        moneylender (ForeignKey): Relación con el prestamista (`Moneylender`) que otorga el préstamo.
        total_debt_paid (DecimalField): Cantidad total que el prestatario ha pagado hasta la fecha.
        amount_to_pay (DecimalField): Cantidad pendiente de pago por parte del prestatario.
        start_date (DateField): Fecha de inicio del préstamo, que indica cuándo el préstamo se activó.
    """
    id = models.AutoField(primary_key=True)  # ID único del préstamo activo
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)  # Relación con el modelo Loans
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)  # Relación con el modelo Borrower (quien recibe el dinero)
    moneylender = models.ForeignKey(Moneylender, on_delete=models.CASCADE)  # Relación con el modelo Moneylender (quien presta el dinero) 
    total_debt_paid = models.DecimalField(max_digits=10, decimal_places=2)  # Cantidad pagada por el prestatario
    amount_to_pay = models.DecimalField(max_digits=10, decimal_places=2)  # Cantidad pendiente de pagar
    start_date = models.DateField(null=True) #Fecha de inicio del prestamo 

class Payments(models.Model):
    """
    Modelo que representa los pagos asociados a un préstamo activo.

    Este modelo almacena la información sobre cada pago programado para un préstamo activo. 
    Incluye detalles como la fecha límite de pago, el estado del pago, y si el pago fue realizado 
    dentro del plazo establecido.

    Atributos:
        id (int): ID único del pago.
        active_loan (ForeignKey): Relación con el modelo `ActiveLoan` al que pertenece el pago.
        number_of_pay (int): Número que identifica el orden del pago dentro del calendario de pagos del préstamo.
        date_to_pay (DateField): Fecha límite en la que debe realizarse el pago.
        paid (BooleanField): Indica si el pago ya ha sido realizado (`True`) o no (`False`). Puede ser `null` si no se ha actualizado.
        paid_on_time (BooleanField): Indica si el pago fue realizado dentro de la fecha límite (`True`) o fuera de ella (`False`). Puede ser `null` si no se ha actualizado.
    """
    id = models.AutoField(primary_key=True)
    active_loan = models.ForeignKey(ActiveLoan, on_delete=models.CASCADE, related_name='payments')
    number_of_pay = models.IntegerField() #Numero que identifica el numero de pago
    date_to_pay = models.DateField() #Fecha limite en que se tiene que hacer el pago 
    paid = models.BooleanField(null=True) # Indicador si ya se pago o no 
    paid_on_time = models.BooleanField(null=True) # Indicador si se pago en la fecha o no
    
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
