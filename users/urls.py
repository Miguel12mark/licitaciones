from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import perfil, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('perfil/', perfil),
    path('', include(router.urls)),
]