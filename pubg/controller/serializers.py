from rest_framework import serializers
from accounts.models import BaseOrder
from booster.models import Booster

class DivisionSerializer(serializers.Serializer):
    current_rank        = serializers.IntegerField(min_value=1, max_value=10)
    current_division    = serializers.IntegerField(min_value=1, max_value=5)
    marks               = serializers.IntegerField(min_value=0, max_value=4)
    desired_rank        = serializers.IntegerField(min_value=1, max_value=10)
    desired_division    = serializers.IntegerField(min_value=1, max_value=5)

    duo_boosting        = serializers.BooleanField()
    select_booster      = serializers.BooleanField()
    turbo_boost         = serializers.BooleanField()
    streaming           = serializers.BooleanField()

    price               = serializers.FloatField(min_value=10)
    choose_booster      = serializers.IntegerField()
    extend_order        = serializers.IntegerField()

    promo_code          = serializers.CharField()
    server              = serializers.CharField()

    def validate(self, attrs):
        self.booster_validate(attrs)
        self.extend_order_validate(attrs)
        return attrs

    def booster_validate(self, attrs):
        choose_booster = attrs.get('choose_booster', '')
        select_booster = attrs.get('select_booster', '')
        if choose_booster > 0 and select_booster:
            try :
                Booster.objects.get(booster_id = choose_booster, is_pubg_player= True, can_choose_me= True)
            except Booster.DoesNotExist:
                raise serializers.ValidationError("This Booster is not belong to Pubg Mobile.")    
            
    def extend_order_validate(self, attrs):
        extend_order = attrs.get('extend_order', '')
        if extend_order > 0:
            try:
                BaseOrder.objects.get(id=extend_order, game__id=3, game_type='D')
            except BaseOrder.DoesNotExist:
                raise serializers.ValidationError("This order can't be extended")        

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if data['select_booster'] == False  :
            data['choose_booster'] = 0
        return data