from rest_framework import serializers
from .models import Licitacion, LicitacionProducto
from productos.models import Producto
from clientes.models import Cliente

# 🔗 Serializer intermedio
class LicitacionProductoSerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = LicitacionProducto
        fields = '__all__'
        read_only_fields = ('subtotal',)

    def get_subtotal(self, obj):
        return obj.subtotal()


# 📑 Serializer principal
class LicitacionSerializer(serializers.ModelSerializer):
    productos = LicitacionProductoSerializer(
        source='licitacionproducto_set',
        many=True,
        read_only=True
    )

    total = serializers.SerializerMethodField()

    class Meta:
        model = Licitacion
        fields = '__all__'
     
     
    def validate_cliente(self, value):
        if not Cliente.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Cliente no existe")
        return value
    def validate_presupuesto_maximo(self, value):
        if value <= 0:
            raise serializers.ValidationError("El presupuesto debe ser mayor a 0")
        return value
       
    def get_total(self, obj):
        return sum(
            lp.cantidad * lp.precio_unitario
            for lp in obj.licitacionproducto_set.all()
        )


# 🔥 Serializer para agregar productos
class AddProductoSerializer(serializers.Serializer):
    producto_id = serializers.IntegerField()
    cantidad = serializers.IntegerField()

    def validate(self, attrs):
        licitacion = self.context.get('licitacion')

        if not licitacion:
            raise serializers.ValidationError("Licitación no encontrada en contexto")

        try:
            producto = Producto.objects.get(id=attrs['producto_id'])
        except Producto.DoesNotExist as exc:
            raise serializers.ValidationError("Producto no existe") from exc

        if attrs['cantidad'] <= 0:
            raise serializers.ValidationError("Cantidad debe ser mayor a 0")

        subtotal = producto.precio * attrs['cantidad']

        total_actual = sum(
            lp.subtotal()
            for lp in licitacion.licitacionproducto_set.all()
        )

        if total_actual + subtotal > licitacion.presupuesto_maximo:
            raise serializers.ValidationError(
                "Se excede el presupuesto máximo"
            )

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