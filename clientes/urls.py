from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ClienteViewSet, clientes_view

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='clientes')

urlpatterns = [
    # 🔥 HTML
    path('clientes-view/', clientes_view),

    # 🔗 API
    path('', include(router.urls)),
]
