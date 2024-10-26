from rest_framework import serializers

class ScoreSerializer(serializers.Serializer):

    Monto=serializers.CharField(max_length=100)
    N_CuotasS=serializers.CharField(max_length=100)
    Pagos_Fuera_Fecha=serializers.CharField(max_length=100)
    Total=serializers.CharField(max_length=100)
    Operacion=serializers.ChoiceField(choices=[("aumentar_Score", "aumentar_Score"), ("reducir_Score", "reducir_Score")])