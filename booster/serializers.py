# serializers.py
from rest_framework import serializers
from booster.models import Rating

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['rate', 'text', 'anonymous']