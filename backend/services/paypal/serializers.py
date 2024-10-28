

from rest_framework import serializers



class PaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3)

class PayoutSerializer(serializers.Serializer):
    recipient_email = serializers.EmailField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3, default='USD')
    

#Serializer para crear produtos (1 solo uso)
class PayPalProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    type = serializers.ChoiceField(choices=[("SERVICE", "Service"), ("PRODUCT", "Product")])
    category = serializers.CharField(max_length=100)
