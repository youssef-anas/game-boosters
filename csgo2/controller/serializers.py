from rest_framework import serializers
from accounts.models import BaseOrder
from booster.models import Booster

class DivisionSerializer(serializers.Serializer):
    current_rank = serializers.IntegerField(min_value=1, max_value=17)
    desired_rank = serializers.IntegerField(min_value=1, max_value=18)

    server = serializers.CharField(max_length=300)
    price = serializers.FloatField(min_value=10)
    promo_code = serializers.CharField()

    duo_boosting = serializers.BooleanField()
    select_booster = serializers.BooleanField()
    turbo_boost = serializers.BooleanField()
    streaming = serializers.BooleanField()

    choose_booster = serializers.IntegerField()
    extend_order = serializers.IntegerField()

    def validate(self, attrs):
        self.extend_order_validate(attrs)
        self.booster_validate(attrs)
        return attrs
    
    def extend_order_validate(self, attrs):
        extend_order = attrs.get('extend_order', '')
        if extend_order > 0:
            try:
                BaseOrder.objects.get(id=extend_order, game__id=2, game_type='D')
            except BaseOrder.DoesNotExist:
                raise serializers.ValidationError("This order can't be extended")
  
            
    def booster_validate(self, attrs):
        choose_booster = attrs.get('choose_booster', '')
        select_booster = attrs.get('select_booster', '')
        if choose_booster > 0 and select_booster:
            try :
                Booster.objects.get(booster_id = choose_booster, is_csgo2_player= True, can_choose_me= True)
            except Booster.DoesNotExist:
                raise serializers.ValidationError("This Booster is not belong to Csgo2.")
            
    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        if data['choose_booster'] and data['select_booster'] :
            data['choose_booster'] = 'another_value'

        return data            