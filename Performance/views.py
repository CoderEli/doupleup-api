from rest_framework import viewsets
from .models import PerformanceMetric
from .serializers import PerformanceMetricSerializer
from rest_framework.permissions import IsAuthenticated

class PerformanceMetricViewSet(viewsets.ModelViewSet):
    queryset = PerformanceMetric.objects.all()
    serializer_class = PerformanceMetricSerializer
    permission_classes = [IsAuthenticated]
