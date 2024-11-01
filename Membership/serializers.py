from rest_framework import serializers
from .models import MembershipFee

class MembershipFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipFee
        fields = '__all__'
