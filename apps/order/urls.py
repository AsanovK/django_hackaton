from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register('', OrderViewSet)

urlpatterns = []
urlpatterns.extend(router.urls)