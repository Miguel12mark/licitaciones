from django.contrib import admin
from django.urls import path, include

from users.views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from .views import home

urlpatterns = [
    path('', home),
    
    path('admin/', admin.site.urls),

    # 🔐 AUTH
    path('api/token/', CustomTokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),

    # 📦 APPS
    path('api/', include('users.urls')),
    path('api/', include('clientes.urls')),
    path('api/', include('productos.urls')),
    path('api/', include('licitaciones.urls')),
]