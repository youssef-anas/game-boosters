from rest_framework import serializers
from accounts.models import BaseOrder
from booster.models import Booster

class DivisionSerializer(serializers.Serializer):
    current_rank            = serializers.IntegerField(min_value=1, max_value=7)
    current_division        = serializers.IntegerField(min_value=1, max_value=4)
    marks                   = serializers.IntegerField(min_value=0, max_value=4)
    desired_rank            = serializers.IntegerField(min_value=1, max_value=8)
    desired_division        = serializers.IntegerField(min_value=1, max_value=4)

    duo_boosting            = serializers.BooleanField()
    streaming               = serializers.BooleanField()
    turbo_boost             = serializers.BooleanField()
    select_booster          = serializers.BooleanField()

    server                  = serializers.CharField(max_length=300)
    price                   = serializers.FloatField(min_value=10)
    choose_booster          = serializers.IntegerField()
    extend_order            = serializers.IntegerField()
    promo_code              = serializers.CharField()

    def validate(self, attrs):
        self.booster_validate(attrs)
        self.extend_order_validate(attrs)
        return attrs

    def booster_validate(self, attrs):
        choose_booster = attrs.get('choose_booster', '')
        select_booster = attrs.get('select_booster', '')
        if choose_booster > 0 and select_booster:
            try :
                Booster.objects.get(booster_id = choose_booster, is_tft_player= True, can_choose_me= True)
            except Booster.DoesNotExist:
                raise serializers.ValidationError("This Booster is not belong to Rocket League.")    
            
    def extend_order_validate(self, attrs):
        extend_order = attrs.get('extend_order', '')
        if extend_order > 0:
            try:
                BaseOrder.objects.get(id=extend_order, game__id=5, game_type='D')
            except BaseOrder.DoesNotExist:
                raise serializers.ValidationError("This order can't be extended")        

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if data['select_booster'] == False  :
            data['choose_booster'] = 0
        return data


class PlacementSerializer(serializers.Serializer):
    last_rank               = serializers.IntegerField(min_value=0, max_value=8)
    number_of_match         = serializers.IntegerField(min_value=1, max_value=5)

    duo_boosting            = serializers.BooleanField()
    select_booster          = serializers.BooleanField()
    turbo_boost             = serializers.BooleanField()
    streaming               = serializers.BooleanField()

    server                  = serializers.CharField(max_length=300)
    price                   = serializers.FloatField(min_value=10)
    choose_booster          = serializers.IntegerField()
    promo_code              = serializers.CharField()

    def validate(self, attrs):
        self.booster_validate(attrs)
        return attrs

    def booster_validate(self, attrs):
        choose_booster = attrs.get('choose_booster', '')
        select_booster = attrs.get('select_booster', '')
        if choose_booster > 0 and select_booster:
            try :
                Booster.objects.get(booster_id = choose_booster, is_tft_player= True, can_choose_me= True)
            except Booster.DoesNotExist:
                raise serializers.ValidationError("This Booster is not belong to Team Fight Tactics.")     

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if data['select_booster'] == False  :
            data['choose_booster'] = 0
        return data