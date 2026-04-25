from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from .models import Licitacion
from .serializers import (
    LicitacionSerializer,
    AddProductoSerializer
)


class LicitacionViewSet(viewsets.ModelViewSet):
    queryset = Licitacion.objects.all().order_by('-created_at')
    serializer_class = LicitacionSerializer
    permission_classes = [IsAuthenticated]

    # 🔥 AGREGAR PRODUCTO
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

        return Response({"message": "Producto agregado correctamente"}, status=status.HTTP_201_CREATED)

    # 🔥 CAMBIAR ESTADO
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

        # 🚨 REGLA: no reactivar cerradas
        if licitacion.estado in ['finalizada', 'perdida'] and nuevo_estado == 'activa':
            return Response(
                {"error": "No se puede reactivar una licitación cerrada"},
                status=status.HTTP_400_BAD_REQUEST
            )

        licitacion.estado = nuevo_estado
        licitacion.save()

        return Response({"message": "Estado actualizado correctamente"})

    # 🔥 DETALLE (override correcto)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
def licitaciones_view(request):
    licitaciones = Licitacion.objects.all()
    return render(request, 'licitaciones.html', {'licitaciones': licitaciones})