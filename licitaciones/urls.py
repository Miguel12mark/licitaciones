from rest_framework.routers import DefaultRouter
from .views import LicitacionViewSet

router = DefaultRouter()
router.register(r'licitaciones', LicitacionViewSet, basename='licitaciones')

urlpatterns = router.urls