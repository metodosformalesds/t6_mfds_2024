

from rest_framework import serializers



#Serializer para crear produtos (1 solo uso)
class PayPalProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    type = serializers.ChoiceField(choices=[("SERVICE", "Service"), ("PRODUCT", "Product")])
    category = serializers.CharField(max_length=100)
