from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import LicitacionViewSet, licitaciones_view

router = DefaultRouter()
router.register(r'licitaciones', LicitacionViewSet, basename='licitaciones')

urlpatterns = [
    path('licitaciones-view/', licitaciones_view),
    path('', include(router.urls)),
]