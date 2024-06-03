from rest_framework import serializers
from accounts.models import BaseOrder

class BaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseOrder
        fields = ['customer_gamename', 'customer_password', 'customer_username']
