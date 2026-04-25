from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProductoViewSet, productos_view

router = DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='productos')

urlpatterns = [
    # 🔥 HTML
    path('productos-view/', productos_view),

    # 🔗 API
    path('', include(router.urls)),
]