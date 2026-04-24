from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .models import User
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from .permissions import IsAdminUserCustom

from rest_framework_simplejwt.views import TokenObtainPairView


# 🔐 LOGIN JWT CON EMAIL
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# 👤 PERFIL DEL USUARIO LOGUEADO
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil(request):
    return Response({
        "email": request.user.email,
        "role": request.user.role
    })


# 👥 VIEWSET DE USUARIOS
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAdminUserCustom()]  # permitir creación sin auth (solo para bootstrap)
        return [IsAuthenticated()]

    # 🔥 OPCIONAL: QUE EL USER SOLO SE VEA A SÍ MISMO
    def get_queryset(self):
        user = self.request.user

        if user.role == 'admin':
            return User.objects.all()
        return User.objects.filter(id=user.id)

    # 🔥 OPCIONAL: PROTEGER UPDATE / DELETE
    def update(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            return Response(
                {"error": "Solo admin puede actualizar usuarios"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            return Response(
                {"error": "Solo admin puede eliminar usuarios"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)