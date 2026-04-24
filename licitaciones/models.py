from django.db import models
from django.conf import settings
from clientes.models import Cliente
from productos.models import Producto


class Licitacion(models.Model):

    ESTADOS = (
        ('activa', 'Activa'),
        ('finalizada', 'Finalizada'),
        ('por_cobrar', 'Por cobrar'),
        ('perdida', 'Perdida'),
    )

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    presupuesto_maximo = models.DecimalField(max_digits=12, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activa')

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="licitaciones_creadas"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Licitación #{self.pk}"

    # 🔥 REGLA DE NEGOCIO CENTRAL (muy importante)
    def puede_modificarse(self):
        return self.estado == 'activa'
    
class LicitacionProducto(models.Model):
    licitacion = models.ForeignKey(Licitacion, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('licitacion', 'producto')

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"
    