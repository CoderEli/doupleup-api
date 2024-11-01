from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from .views import UserRegistrationView, UserLoginView

router = DefaultRouter()
router.register('profiles', views.UserProfileViewSet)
router.register('membership-status', views.MembershipStatusViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
]
