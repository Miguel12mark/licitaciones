from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Producto
from .serializers import ProductoSerializer
from django.shortcuts import render

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all().order_by('-created_at')
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]
    
def productos_view(request):
    productos = Producto.objects.all()
    return render(request, 'productos.html', {'productos': productos})