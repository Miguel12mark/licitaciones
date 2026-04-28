from django.contrib import admin
from django.urls import path, include

from users.views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from .views import login_view, home, crear_usuario_view

urlpatterns = [
    path('login/', login_view), 
    path('crear-usuario/', crear_usuario_view),
    path('', home),
    path('admin/', admin.site.urls),
    path('api/token/', CustomTokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/', include('users.urls')),
    path('api/', include('clientes.urls')),
    path('api/', include('productos.urls')),
    path('api/', include('licitaciones.urls')),
    path('', include('clientes.urls')),
    path('', include('productos.urls')),
    path('', include('licitaciones.urls')),
]