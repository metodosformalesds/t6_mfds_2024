from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import  CreditHistory, Moneylender, Loan, Borrower, ActiveLoan, InvoiceHistory, Payments, Request, Transaction
from datetime import timedelta
from dotenv import load_dotenv
import os
from django.db.models import Sum

load_dotenv()
INTEREST_BANK = float(os.getenv('INTEREST_BANK', 28.18))
##from django.contrib.auth.models import User
#Serializer del historial crediticio
User = get_user_model()
class CreditHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditHistory
        fields = '__all__'  # Esto incluye todos los campos del modelo

#serializer del prestamista
class MoneylenderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    class Meta:
        model = Moneylender
        fields = '__all__'

#Serializer de los prestamos
class LoansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
#Serializer de las solicitudes de prestamo
class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'
        
#Serializer del prestatario
class BorrowerSerializer(serializers.ModelSerializer):
    credit_history = CreditHistorySerializer(many=True, read_only=True) 
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = Borrower
        fields = '__all__'
class MoneylenderBorrowerSerializer(serializers.ModelSerializer):
    credit_history = CreditHistorySerializer(many=True, read_only=True) 
    class Meta:
        model = Borrower
        fields = ['id', 'first_name', 'middle_name', 'first_surname', 'second_surname', 'birth_date', 'rfc', 'credit_history']
        
        
class MoneylenderLoansSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    borrower = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = [
            'id', 'amount', 'total_amount', 'difficulty', 'interest_rate', 
            'number_of_payments', 'term', 'duration_loan', 'payment_per_term', 
            'publication_date', 'moneylender', 'status', 'borrower'
        ]

    def get_status(self, obj):
        has_active_loan = ActiveLoan.objects.filter(loan=obj).exists()
        return 'En préstamo' if has_active_loan else 'Disponible'

    def get_borrower(self, obj):
        active_loan = ActiveLoan.objects.filter(loan=obj).first()
        if active_loan:
            return MoneylenderBorrowerSerializer(active_loan.borrower).data
        return None

   
#Serializer de los detalles de los prestamos
class ActiveLoansSerializer(serializers.ModelSerializer):
    """
    Serializer para mostrar la información de un préstamo activo junto con 
    los detalles del prestatario y los pagos relacionados. Diseñado para ser
    consumido por el frontend, permitiendo que el prestamista visualice datos clave.

    Atributos:
        borrower (MoneylenderBorrowerSerializer): Información del prestatario.
        payments (SerializerMethodField): Lista de pagos relacionados con el préstamo.
        loan_amount (SerializerMethodField): Monto total del préstamo relacionado.

    Campos del Meta:
        - id: ID único del préstamo activo.
        - borrower: Información del prestatario (nombre, apellidos, etc.).
        - loan_amount: Monto total del préstamo.
        - total_debt_paid: Cantidad total pagada hasta la fecha.
        - amount_to_pay: Cantidad pendiente de pago.
        - start_date: Fecha en la que inició el préstamo.
        - payments: Lista de pagos realizados y pendientes.

    Métodos:
        get_borrower_name: 
            Devuelve el nombre completo del prestatario concatenando 
            su nombre y apellido. (No se utiliza directamente en los campos actuales).
        get_payments: 
            Genera una lista de pagos relacionados al préstamo activo, 
            incluyendo número de pago, fecha, estado del pago y si se realizó a tiempo.
        get_loan_amount: 
            Obtiene el monto total del préstamo desde el modelo relacionado `Loan`.

    Uso:
        Este serializer está diseñado para ayudar al prestamista a gestionar 
        y visualizar detalles sobre préstamos activos y su estado en un sistema 
        frontend.
    """
    borrower = MoneylenderBorrowerSerializer( read_only=True) 
    payments = serializers.SerializerMethodField()
    loan_amount = serializers.SerializerMethodField()
    class Meta:
        model = ActiveLoan
        fields = [
            'id',
            'borrower',       # Nombre del prestatario
            'loan_amount',        # Monto total del préstamo
            'total_debt_paid',     # Cantidad total pagada
            'amount_to_pay',       # Cantidad pendiente
            'start_date',          # Fecha de inicio del préstamo
            'payments',            # Lista de pagos
        ]

    def get_borrower_name(self, obj):
        # Concatenar el nombre completo del prestatario
        return f"{obj.borrower.first_name} {obj.borrower.first_surname}"

    def get_payments(self, obj):
        # Obtener la información de los pagos relacionados
        payments = obj.payments.all()  # Usar el related_name definido en Payments
        return [
            {
                "number_of_pay": payment.number_of_pay,
                "date_to_pay": payment.date_to_pay,
                "paid": payment.paid,
                "paid_on_time": payment.paid_on_time,
            }
            for payment in payments
        ]
    
    def get_loan_amount(self, obj):
        # Obtener el monto total del préstamo desde el modelo relacionado `Loan`
        return obj.loan.amount
        
#Serializer del historial de facturas
class InvoiceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceHistory
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'
        
#Serializer de los detalles de los prestamos
class ActiveLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveLoan
        fields = '__all__'
        
#Serializer de las solicitudes transaccionadas
class TransactionSerializer(serializers.ModelSerializer):
    # Sobrescribir 'payment_date' para mostrar solo la fecha
    payment_date = serializers.SerializerMethodField()
    class Meta:
        model = Transaction
        fields = '__all__'

    def get_payment_date(self, obj):
        return obj.payment_date.date()  # Esto devuelve solo la fecha (sin hora)


class BorrowerMoneylenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moneylender
        fields = ['id', 'first_name','middle_name', 'first_surname', 'second_surname', 'birth_date', 'phone_number', 'rfc'] 

class BorrowerLoanSerializer(serializers.ModelSerializer):
    request_status = serializers.SerializerMethodField()  
    moneylender= BorrowerMoneylenderSerializer(read_only=True) 
    
    class Meta:
        model = Loan
        fields = [
            'id',
            'moneylender',
            'amount',
            'total_amount',
            'difficulty',
            'interest_rate',
            'number_of_payments',
            'term',
            'publication_date',
            'payment_per_term',
            'moneylender',
            'request_status'
        ]
        
    def get_request_status(self, obj):
        borrower_id = self.context.get('borrower_id')  

        # Filtrar las solicitudes del Borrower para cada préstamo 
        request = Request.objects.filter(loan=obj, borrower_id=borrower_id).first()

        if request:
            return request.status  # Retorna el estado si existe
        return ''  
    


class MoneylenderRequestsSerializer(serializers.ModelSerializer):
    borrower = MoneylenderBorrowerSerializer(read_only=True)
    loan = LoansSerializer(read_only=True) 

    class Meta:
        model = Request
        fields = ['id', 'borrower', 'loan', 'status', 'created_at']  
        
class MoneylenderLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['amount', 'interest_rate', 'number_of_payments', 'term']

    # Validar la tasa de interés
    def validate_interest_rate(self, value):
        if value > INTEREST_BANK:
            raise serializers.ValidationError(f"La tasa de interés no puede exceder el {INTEREST_BANK}%")
        return value

    # Validar el monto del préstamo
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("El monto del préstamo debe ser mayor que 0")
        return value

    # Validar el número de pagos
    def validate_number_of_payments(self, value):
        if value <= 0:
            raise serializers.ValidationError("El número de pagos debe ser mayor que 0")
        return value

    # Validación de varios campos
    def validate(self, data):
        # Ejemplo: Validar que el número de pagos y el término sean consistentes
        if data['term'] == 1 and data['number_of_payments'] > 52:  # Semanalmente, máximo 52 semanas
            raise serializers.ValidationError("Número de pagos no puede exceder las 52 semanas en plazo semanal")
        if data['term'] == 2 and data['number_of_payments'] > 24:  # Quincenalmente, máximo 24 quincenas
            raise serializers.ValidationError("Número de pagos no puede exceder las 24 quincenas en plazo quincenal")
        if data['term'] == 3 and data['number_of_payments'] > 12:  # Mensual, máximo 12 meses
            raise serializers.ValidationError("Número de pagos no puede exceder los 12 meses en plazo mensual")

        return data
class BorrowerCreditHistorySerializer(serializers.ModelSerializer):
    credit_history = CreditHistorySerializer(many=True, read_only=True)  
    class Meta:
        model = Borrower
        fields = [
            'first_name', 'middle_name', 'first_surname', 'second_surname', 'credit_history', 'rfc'
        ]

class BorrowerRequestSerializer(serializers.ModelSerializer):
    moneylender_id = serializers.IntegerField()
    loan_id = serializers.IntegerField()
    class Meta:
        model = Request
        fields = ['moneylender_id', 'loan_id']
        
        
class BorrowerActiveLoanSerializer(serializers.ModelSerializer):
    moneylender = BorrowerMoneylenderSerializer(read_only=True)  # Serializer for related Moneylender
    loan = LoansSerializer(read_only=True)  # Serializer for related Loan
    payments = PaymentSerializer(many=True, read_only=True)
    
    class Meta:
        model = ActiveLoan
        fields = [
            'id',
             #Campos de ActiveLoan
            'total_debt_paid',
            'amount_to_pay',
            'start_date',
            'loan',
            'moneylender',
            'payments',
        ]
class MoneylenderTransactionSerializer(serializers.ModelSerializer):
    transactions = serializers.SerializerMethodField()
    
    class Meta:
        model = Moneylender
        fields = ['transactions']

    def get_transactions(self, obj):
        # Obtener las transacciones asociadas al Moneylender
        active_loans = ActiveLoan.objects.filter(moneylender=obj)
        transactions = Transaction.objects.filter(active_loan__in=active_loans)

        # Serializar cada transacción
        transaction_data = []
        for transaction in transactions:
            # Determinar la persona asociada a la transacción
            if transaction.transaction_type == 'payout':
                person_data = {
                    'id': transaction.active_loan.moneylender.id,
                    'first_name': transaction.active_loan.moneylender.first_name,
                    'middle_name': transaction.active_loan.moneylender.middle_name,
                    'first_surname': transaction.active_loan.moneylender.first_surname,
                    'second_surname': transaction.active_loan.moneylender.second_surname,
                    'rfc': transaction.active_loan.moneylender.rfc,
                }
            elif transaction.transaction_type == 'payment':
                person_data = {
                    'id': transaction.active_loan.borrower.id,
                    'first_name': transaction.active_loan.borrower.first_name,
                    'middle_name': transaction.active_loan.borrower.middle_name,
                    'first_surname': transaction.active_loan.borrower.first_surname,
                    'second_surname': transaction.active_loan.borrower.second_surname,
                    'rfc': transaction.active_loan.borrower.rfc,
                }
            else:
                person_data = {}

            transaction_data.append({
                'id': transaction.id,
                'amount_paid': transaction.amount_paid,
                'payment_date': transaction.payment_date,
                'transaction_type': transaction.transaction_type,
                'status': transaction.status,
                'paypal_transaction_id': transaction.paypal_transaction_id,
                'person': person_data  
            })

        return transaction_data
    
from django.db.models import Sum

class MoneylenderDetailSerializer(serializers.ModelSerializer):
    """
    Serializer para mostrar detalles específicos de un prestamista, incluyendo 
    estadísticas clave y una lista de préstamos activos asociados.

    Atributos:
        total_loans (SerializerMethodField): Calcula el monto total prestado 
            por el prestamista en todos sus préstamos activos.
        total_earnings (SerializerMethodField): Calcula las ganancias totales 
            del prestamista basadas en el interés generado por sus préstamos activos.
        total_active_loans (SerializerMethodField): Devuelve el número de 
            préstamos activos asociados con el prestamista.
        total_pending_balance (SerializerMethodField): Devuelve el saldo total 
            pendiente por cobrar en los préstamos activos.
        active_loans (SerializerMethodField): Devuelve una lista detallada de 
            los préstamos activos del prestamista, serializados con `ActiveLoansSerializer`.

    Campos del Meta:
        - id: ID único del prestamista.
        - first_name: Nombre del prestamista.
        - total_loans: Monto total prestado por el prestamista.
        - total_earnings: Ganancias totales generadas por intereses.
        - total_active_loans: Cantidad de préstamos activos en curso.
        - total_pending_balance: Saldo pendiente por cobrar en préstamos.
        - active_loans: Lista serializada de préstamos activos.

    Métodos:
        get_total_loans(obj):
            Calcula el monto total prestado por el prestamista sumando 
            los montos de los préstamos activos asociados.

        get_total_earnings(obj):
            Calcula las ganancias totales generadas por los préstamos activos, 
            basándose en el interés aplicado a cada préstamo.

        get_total_active_loans(obj):
            Cuenta el número total de préstamos activos asociados al prestamista.

        get_total_pending_balance(obj):
            Calcula el saldo total pendiente por cobrar sumando el valor 
            `amount_to_pay` de todos los préstamos activos.

        get_active_loans(obj):
            Devuelve una lista serializada de los préstamos activos relacionados 
            con el prestamista, utilizando el `ActiveLoansSerializer`.

    Uso:
        Este serializer está diseñado para proveer una vista consolidada de 
        las estadísticas y datos relevantes para un prestamista en un sistema 
        de préstamos. Ideal para endpoints que sirven datos al frontend 
        o para reportes administrativos.
    """
    total_loans = serializers.SerializerMethodField()
    total_earnings = serializers.SerializerMethodField()
    total_active_loans = serializers.SerializerMethodField()
    total_pending_balance = serializers.SerializerMethodField()
    active_loans = serializers.SerializerMethodField()

    class Meta:
        model = Moneylender
        fields = [
            'id',
            'first_name',
            'total_loans',            # Monto total prestado
            'total_earnings',          # Ganancias totales
            'total_active_loans',      # Número de préstamos activos
            'total_pending_balance',   # Saldo pendiente
            'active_loans',            # Lista de préstamos activos
        ]

    def get_total_loans(self, obj):
        """
        Calcula el monto total prestado por el prestamista.

        Parámetros:
        obj (Moneylender): Instancia del modelo Moneylender.

        Proceso:
            - Filtra los préstamos activos (`ActiveLoan`) asociados al prestamista (`moneylender=obj`).
            - Usa la función de agregación `Sum` para sumar el monto de los préstamos (`loan__amount`).
            - Si no hay préstamos registrados, devuelve 0 por defecto.

        Retorna:
            float: La suma total del monto prestado.
        """
        return ActiveLoan.objects.filter(moneylender=obj).aggregate(total_loans=Sum('loan__amount'))['total_loans'] or 0

    def get_total_earnings(self, obj):
        """
        Calcula las ganancias totales del prestamista.

        Parámetros:
        obj (Moneylender): Instancia del modelo Moneylender.

        Proceso:
            - Filtra los préstamos activos (`ActiveLoan`) asociados al prestamista (`moneylender=obj`).
            - Calcula el interés generado en cada préstamo:            - Se toma el monto del préstamo (`loan.amount`).
            - Se multiplica por la tasa de interés (`loan.interest_rate`) y se divide entre 100.
            - Suma los intereses generados de todos los préstamos.

        Retorna:
            float: El total de las ganancias generadas por intereses.
    """
        # Calcular el interés total generado en cada préstamo activo del prestamista
        loans = ActiveLoan.objects.filter(moneylender=obj)
        total_earnings = sum(loan.loan.amount * loan.loan.interest_rate / 100 for loan in loans)
        return float(total_earnings)  # Asegurarse de que sea un valor serializable en JSON

    def get_total_active_loans(self, obj):
        """
        Cuenta el número total de préstamos activos del prestamista.

        Parámetros:
            obj (Moneylender): Instancia del modelo Moneylender.

        Proceso:
            - Filtra los préstamos activos (`ActiveLoan`) asociados al prestamista (`moneylender=obj`).
            - Usa la función `count()` para contar los registros encontrados.

        Retorna:    
            int: El número total de préstamos activos.
        """
        # Contar el número de préstamos activos
        return ActiveLoan.objects.filter(moneylender=obj).count()

    def get_total_pending_balance(self, obj):
        """
        Calcula el saldo total pendiente de todos los préstamos activos del prestamista.

        Parámetros:
            obj (Moneylender): Instancia del modelo Moneylender.

        Proceso:
            - Filtra los préstamos activos (`ActiveLoan`) asociados al prestamista (`moneylender=obj`).
            - Usa la función de agregación `Sum` para sumar el monto pendiente (`amount_to_pay`).
            - Si no hay registros, devuelve 0 por defecto.

        Retorna:
            float: El saldo pendiente total.
        """
        total_pending = ActiveLoan.objects.filter(moneylender=obj).aggregate(total_pending=Sum('amount_to_pay'))['total_pending'] or 0
        return float(total_pending)  # Asegurarse de que sea un valor serializable en JSON

    def get_active_loans(self, obj):
        """
        Serializa la información de los préstamos activos del prestamista.

        Parámetros:
            obj (Moneylender): Instancia del modelo Moneylender.

        Proceso:
            - Filtra los préstamos activos (`ActiveLoan`) asociados al prestamista (`moneylender=obj`).
            - Usa el serializer `ActiveLoansSerializer` para serializar los datos de los préstamos.

        Retorna:
            list: Una lista de datos serializados de los préstamos activos.
        """
        # Serializar los préstamos activos relacionados con el Moneylender
        active_loans = ActiveLoan.objects.filter(moneylender=obj)
        return ActiveLoansSerializer(active_loans, many=True).data 
    
    
class LoanHistorySerializer(serializers.ModelSerializer):
    """
    Serializador para la clase ActiveLoan, utilizado para estructurar los datos que se enviarán al frontend
    en la vista de historial de préstamos. Este serializador incluye información detallada sobre el historial de
    préstamos como montos, intereses, términos, fechas y estado.
    """
    moneylender_name = serializers.SerializerMethodField()
    borrower_name = serializers.SerializerMethodField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, source='loan.amount')
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, source='loan.total_amount')
    payment_per_term = serializers.DecimalField(max_digits=10, decimal_places=2, source='loan.payment_per_term')
    term_type = serializers.SerializerMethodField()
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2, source='loan.interest_rate')
    number_of_payments = serializers.IntegerField(source='loan.number_of_payments')
    on_time_payments = serializers.SerializerMethodField()
    late_payments = serializers.SerializerMethodField()
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = ActiveLoan
        fields = [
            'id', 'moneylender_name', 'borrower_name', 'amount', 'total_amount', 'payment_per_term', 'term_type',
            'interest_rate', 'number_of_payments', 'on_time_payments', 'late_payments',
            'start_date', 'end_date', 'status'
        ]
            
    def get_moneylender_name(self, obj):
        """
        Obtiene el nombre completo del prestamista.

        Parámetros:
            obj: Instancia de ActiveLoan.

        Retorna:
            str: Nombre completo del prestamista en formato "Nombre Apellido".
        """
        moneylender = obj.moneylender
        return f"{moneylender.first_name} {moneylender.first_surname}"

    def get_borrower_name(self, obj):
        """
        Obtiene el nombre completo del prestatario.

        Parámetros:
            obj: Instancia de ActiveLoan.

        Retorna:
            str: Nombre completo del prestatario en formato "Nombre Apellido1 Apellido2".
        """
        borrower = obj.borrower
        return f"{borrower.first_name} {borrower.first_surname} {borrower.second_surname}"

    def get_term_type(self, obj):
        """
        Traduce el término del préstamo a su representación textual.

        Parámetros:
            obj: Instancia de ActiveLoan.

        Retorna:
            str: Representación textual del término (Semanal, Quincenal, Mensual) o 'Desconocido' si no se encuentra.
        """
        term_dict = {1: 'Semanal', 2: 'Quincenal', 3: 'Mensual'}
        return term_dict.get(obj.loan.term, 'Desconocido')

    def get_on_time_payments(self, obj):
        """
        Calcula la cantidad de pagos realizados a tiempo.

        Parámetros:
            obj: Instancia de ActiveLoan.

        Retorna:
            int: Número de pagos que tienen `paid=True` y `paid_on_time=True`.
        """
        return obj.payments.filter(paid=True, paid_on_time=True).count()

    def get_late_payments(self, obj):
        """
        Calcula la cantidad de pagos realizados tarde.

        Parámetros:
            obj: Instancia de ActiveLoan.

        Retorna:
            int: Número de pagos que tienen `paid=True` y `paid_on_time=False`.
        """
        return obj.payments.filter(paid=True, paid_on_time=False).count()

    def get_start_date(self, obj):
        """
        Obtiene la fecha del primer pago registrado para el préstamo.

        Parámetros:
            obj: Instancia de ActiveLoan.

        Retorna:
            date: Fecha del primer pago (campo `date_to_pay`) o None si no hay pagos registrados.
        """
        first_payment = obj.payments.order_by('date_to_pay').first()
        return first_payment.date_to_pay if first_payment else None

    def get_end_date(self, obj):
        """
        Obtiene la fecha del último pago registrado para el préstamo.

        Parámetros:
            obj: Instancia de ActiveLoan.

        Retorna:
            date: Fecha del último pago (campo `date_to_pay`) o None si no hay pagos registrados.
        """
        last_payment = obj.payments.order_by('date_to_pay').last()
        return last_payment.date_to_pay if last_payment else None  

    def get_status(self, obj):
        """
        Determina el estado del préstamo basado en el monto pendiente de pago.

        Parámetros:
            obj: Instancia de ActiveLoan.

        Retorna:
            str: Estado del préstamo. Puede ser:
                - 'Pagado': Si el monto pendiente de pago (`amount_to_pay`) es 0.
                - 'En curso': Si hay montos pendientes mayores a 0.
        """
        if obj.amount_to_pay == 0:
            return 'Pagado'
        elif obj.amount_to_pay > 0:
            return 'En curso'