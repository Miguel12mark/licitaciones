from django.db import models
from django.core.exceptions import ValidationError


class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
        if self.precio <= 0:
            raise ValidationError("El precio debe ser mayor a 0")

    def save(self, *args, **kwargs):
        self.full_clean()  # 🔥 esto ejecuta clean()
        super().save(*args, **kwargs)

    def __str__(self): # pylint: disable=invalid-str-returned
        return self.nombre