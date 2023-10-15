from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SensorViewSet
from . import views

router = DefaultRouter()
router.register('sensors', SensorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('measurements/', include(router.urls)),
    
]