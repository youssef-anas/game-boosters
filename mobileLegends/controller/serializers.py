from rest_framework import serializers
from accounts.models import BaseOrder
from booster.models import Booster

class DivisionSerializer(serializers.Serializer):
    current_rank        = serializers.IntegerField(min_value=1, max_value=9)
    current_division    = serializers.IntegerField(min_value=1, max_value=5)
    marks               = serializers.IntegerField(min_value=0, max_value=5)
    desired_rank        = serializers.IntegerField(min_value=1, max_value=10)
    desired_division    = serializers.IntegerField(min_value=1, max_value=5)
    duo_boosting        = serializers.BooleanField()
    select_booster      = serializers.BooleanField()
    turbo_boost         = serializers.BooleanField()
    streaming           = serializers.BooleanField()
    price               = serializers.FloatField(min_value=10)
    select_champion     = serializers.BooleanField()
    choose_booster      = serializers.IntegerField()
    extend_order        = serializers.IntegerField()
    promo_code          = serializers.CharField()
    server              = serializers.CharField()

    def validate(self, attrs):
        self.extend_order_validate(attrs)
        self.booster_validate(attrs)
        return attrs
        
    def extend_order_validate(self, attrs):
        extend_order = attrs.get('extend_order', '')
        if extend_order > 0:
            try:
                BaseOrder.objects.get(id=extend_order, game__id=8, game_type='D')
            except BaseOrder.DoesNotExist:
                raise serializers.ValidationError("This order can't be extended")

            
    def booster_validate(self, attrs):
        choose_booster = attrs.get('choose_booster', '')
        select_booster = attrs.get('select_booster', '')
        if choose_booster > 0 and select_booster:
            try :
                Booster.objects.get(booster_id = choose_booster, is_mobleg_player= True, can_choose_me= True)
            except Booster.DoesNotExist:
                raise serializers.ValidationError("This Booster is not belong to Mobile Legends.")
            
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if data['select_booster'] == False  :
            data['choose_booster'] = 0
        return data   

class PlacementSerializer(serializers.Serializer):
    last_rank           = serializers.IntegerField(min_value=0, max_value=11)
    number_of_match     = serializers.IntegerField(min_value=1, max_value=5)
    promo_code          = serializers.CharField()
    select_booster      = serializers.BooleanField()
    server              = serializers.CharField()
    select_champion     = serializers.BooleanField()
    choose_booster      = serializers.IntegerField()

    def validate(self, attrs):
        self.booster_validate(attrs)
        return attrs

    def booster_validate(self, attrs):
        choose_booster = attrs.get('choose_booster', '')
        select_booster = attrs.get('select_booster', '')
        if choose_booster > 0 and select_booster:
            try :
                Booster.objects.get(booster_id = choose_booster, is_mobleg_player= True, can_choose_me= True)
            except Booster.DoesNotExist:
                raise serializers.ValidationError("This Booster is not belong to Mobile Legends.")
            
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if data['select_booster'] == False  :
            data['choose_booster'] = 0
        return data   
