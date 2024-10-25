from rest_framework import serializers
from database.models import Borrower

class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = '__all__'