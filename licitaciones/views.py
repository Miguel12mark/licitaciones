from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Licitacion
from .serializers import LicitacionSerializer, AddProductoSerializer


def licitaciones_view(request):
    return render(request, 'licitaciones.html')

class LicitacionViewSet(viewsets.ModelViewSet):
    serializer_class = LicitacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Licitacion.objects.all().order_by('-created_at')

        cliente_id = self.request.query_params.get('cliente')

        if cliente_id:
            queryset = queryset.filter(cliente_id=cliente_id)

        return queryset
    
    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    @action(detail=True, methods=['post'])
    def add_producto(self, request, pk=None):
        licitacion = self.get_object()

        if licitacion.estado != 'activa':
            return Response(
                {"error": "No se pueden agregar productos a una licitación no activa"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AddProductoSerializer(
            data=request.data,
            context={'licitacion': licitacion}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "Producto agregado correctamente"})

    @action(detail=True, methods=['patch'])
    def cambiar_estado(self, request, pk=None):
        licitacion = self.get_object()
        nuevo_estado = request.data.get("estado")

        estados_validos = ['activa', 'finalizada', 'por_cobrar', 'perdida']

        if nuevo_estado not in estados_validos:
            return Response(
                {"error": "Estado inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if licitacion.estado in ['finalizada', 'perdida'] and nuevo_estado == 'activa':
            return Response(
                {"error": "No se puede reactivar una licitación cerrada"},
                status=status.HTTP_400_BAD_REQUEST
            )

        licitacion.estado = nuevo_estado
        licitacion.save()

        return Response({"message": "Estado actualizado correctamente"})
    
    @action(detail=True, methods=['get'])
    def productos(self, request, pk=None):
        licitacion = self.get_object()
    
        data = [
            {
                "id": lp.producto.id,
                "nombre": lp.producto.nombre,
                "precio": lp.precio_unitario,
                "cantidad": lp.cantidad,
                "subtotal": lp.cantidad * lp.precio_unitario
            }
            for lp in licitacion.licitacionproducto_set.all()
        ]
    
        return Response(data)