from rest_framework import serializers
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.email', read_only=True)
    updated_by = serializers.CharField(source='updated_by.email', read_only=True)

    class Meta:
        model = Producto
        fields = '__all__'
        
    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a 0")
        return value