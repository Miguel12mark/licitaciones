from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .models import User
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from .permissions import IsAdminUserCustom

from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil(request):
    return Response({
        "email": request.user.email,
        "role": request.user.role
    })

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAdminUserCustom()]  
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'admin':
            return User.objects.all()
        return User.objects.filter(id=user.id)

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