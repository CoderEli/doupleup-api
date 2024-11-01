from rest_framework import viewsets
from .models import MembershipFee
from .serializers import MembershipFeeSerializer
from rest_framework.permissions import IsAuthenticated

class MembershipFeeViewSet(viewsets.ModelViewSet):
    queryset = MembershipFee.objects.all()
    serializer_class = MembershipFeeSerializer
    permission_classes = [IsAuthenticated]
