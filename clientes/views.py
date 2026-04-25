from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Cliente
from .serializers import ClienteSerializer


# 🔹 API (JSON)
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all().order_by('-created_at')
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]


# 🔹 VISTA HTML
def clientes_view(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {
        'clientes': clientes
    })