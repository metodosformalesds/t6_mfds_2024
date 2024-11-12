def calcular_dificultad(loan):
    # Definir coeficientes de ponderación para cada atributo
    coef_monto = 0.3
    coef_interes = 0.2
    coef_num_pagos = 0.2
    coef_plazo = 0.15
    coef_pago_term = 0.15

    # Obtención de los atributos del préstamo
    monto = float(loan.amount)
    tasa_interes = float(loan.interest_rate)
    num_pagos = float(loan.number_of_payments)
    plazo = loan.term
    pago_term = float(loan.payment_per_term)

    # Cálculo de la dificultad
    # Puedes usar una fórmula que pondera estos factores. Aquí hay una fórmula de ejemplo:
    
    dificultad = (
        coef_monto * (monto / 1000) +  # La cantidad del préstamo, normalizada por 1000
        coef_interes * tasa_interes +  # La tasa de interés
        coef_num_pagos * (num_pagos / 12) +  # Número de pagos, normalizado por 12 (considerando el plazo máximo de 12 meses)
        coef_plazo * plazo +  # Plazo (puedes usar 1 para "Semanal", 2 para "Quincenal" y 3 para "Mensual")
        coef_pago_term * (pago_term / monto)  # Proporción de pago por término respecto al monto total
    )

    # Asegúrate de que el puntaje sea razonable
    # Por ejemplo, podrías limitar el puntaje entre 0 y 100.
    dificultad = min(max(dificultad, 0), 100)

    return dificultad