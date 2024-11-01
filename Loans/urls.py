from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register('loan-repayment', views.LoanRepaymentViewSet)
router.register('loan', views.LoanViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
