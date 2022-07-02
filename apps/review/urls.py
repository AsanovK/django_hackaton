from django import urls
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet

router = DefaultRouter()
router.register('', ReviewViewSet)

urlpatterns = []
urlpatterns.extend(router.urls)
