from rest_framework import viewsets
from .models import Loan, LoanRepayment
from .serializers import LoanSerializer, LoanRepaymentSerializer
from rest_framework.permissions import IsAuthenticated

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

class LoanRepaymentViewSet(viewsets.ModelViewSet):
    queryset = LoanRepayment.objects.all()
    serializer_class = LoanRepaymentSerializer
    permission_classes = [IsAuthenticated]
