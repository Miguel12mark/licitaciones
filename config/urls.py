from django.contrib import admin
from django.urls import path, include

from users.views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from .views import login_view, home

urlpatterns = [
    # 🔐 LOGIN
    path('login/', login_view),

    # 🏠 HOME
    path('', home),

    path('admin/', admin.site.urls),

    # 🔐 AUTH API
    path('api/token/', CustomTokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),

    # 🔗 API
    path('api/', include('users.urls')),
    path('api/', include('clientes.urls')),
    path('api/', include('productos.urls')),
    path('api/', include('licitaciones.urls')),

    # 🔥 HTML VIEWS
    path('', include('clientes.urls')),
    path('', include('productos.urls')),
    path('', include('licitaciones.urls')),
]