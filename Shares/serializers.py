from rest_framework import serializers
from .models import Share, SharePurchase

class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = '__all__'

class SharePurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharePurchase
        fields = '__all__'
