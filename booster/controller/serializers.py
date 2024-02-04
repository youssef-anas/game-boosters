# serializers.py
from rest_framework import serializers
from booster.models import Rating
from accounts.models import BaseUser

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['rate', 'text', 'anonymous']

class CanChooseMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ['can_choose_me']