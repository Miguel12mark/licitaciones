from rest_framework import serializers
from .models import Licitacion, LicitacionProducto
from productos.models import Producto


class AuditSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.email', read_only=True)
    updated_by = serializers.CharField(source='updated_by.email', read_only=True)

    class Meta:
        abstract = True


class LicitacionProductoSerializer(AuditSerializer):
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = LicitacionProducto
        fields = '__all__'
        read_only_fields = ('subtotal',)

    def get_subtotal(self, obj):
        return obj.subtotal()



class LicitacionSerializer(AuditSerializer):
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)

    productos = LicitacionProductoSerializer(
        source='licitacionproducto_set',
        many=True,
        read_only=True
    )

    total = serializers.SerializerMethodField()

    class Meta:
        model = Licitacion
        fields = '__all__'

    def validate_presupuesto_maximo(self, value):
        if value <= 0:
            raise serializers.ValidationError("El presupuesto debe ser mayor a 0")
        return value

    def get_total(self, obj):
        return sum(lp.subtotal() for lp in obj.licitacionproducto_set.all())

class AddProductoSerializer(serializers.Serializer):
    producto_id = serializers.IntegerField()
    cantidad = serializers.IntegerField()

    def validate(self, attrs):
        licitacion = self.context.get('licitacion')

        if not licitacion:
            raise serializers.ValidationError("Licitación no encontrada en contexto")

        try:
            producto = Producto.objects.get(id=attrs['producto_id'])
        except Producto.DoesNotExist:
            raise serializers.ValidationError("Producto no existe")

        if attrs['cantidad'] <= 0:
            raise serializers.ValidationError("Cantidad debe ser mayor a 0")

        subtotal = producto.precio * attrs['cantidad']

        total_actual = sum(
            lp.subtotal()
            for lp in licitacion.licitacionproducto_set.all()
        )

        if total_actual + subtotal > licitacion.presupuesto_maximo:
            raise serializers.ValidationError("Se excede el presupuesto máximo")

        attrs['producto'] = producto
        attrs['licitacion'] = licitacion
        attrs['subtotal'] = subtotal

        return attrs

    def create(self, validated_data):
        return LicitacionProducto.objects.create(
            licitacion=validated_data['licitacion'],
            producto=validated_data['producto'],
            cantidad=validated_data['cantidad'],
            precio_unitario=validated_data['producto'].precio
        )