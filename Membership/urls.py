from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register('membership_fee', views.MembershipFeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
