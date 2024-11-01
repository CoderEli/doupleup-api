from rest_framework import viewsets
from .models import Share, SharePurchase
from .serializers import ShareSerializer, SharePurchaseSerializer
from rest_framework.permissions import IsAuthenticated

class ShareViewSet(viewsets.ModelViewSet):
    queryset = Share.objects.all()
    serializer_class = ShareSerializer
    permission_classes = [IsAuthenticated]

class SharePurchaseViewSet(viewsets.ModelViewSet):
    queryset = SharePurchase.objects.all()
    serializer_class = SharePurchaseSerializer
    permission_classes = [IsAuthenticated]
