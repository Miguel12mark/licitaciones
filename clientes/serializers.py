from rest_framework import serializers
from .models import Cliente

class ClienteSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.email', read_only=True)
    updated_by = serializers.CharField(source='updated_by.email', read_only=True)
    class Meta:
        model = Cliente
        fields = '__all__'