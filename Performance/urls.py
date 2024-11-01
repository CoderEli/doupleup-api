from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register('resource-name', views.PerformanceMetricViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
