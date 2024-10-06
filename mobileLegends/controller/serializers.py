from rest_framework import serializers
from accounts.models import BaseOrder
from booster.models import Booster
from ..models import MobileLegendsDivisionOrder, MobileLegendsPlacementOrder
from .order_information import MOBLEG_DOI, MOBLEG_POI

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
    choose_booster      = serializers.IntegerField()
    extend_order        = serializers.IntegerField()
    promo_code          = serializers.CharField()
    server              = serializers.CharField()

    # Order Info
    game_id = serializers.HiddenField(default=8)
    game_type = serializers.HiddenField(default='D')
    game_order_info = MOBLEG_DOI
    order_model = MobileLegendsDivisionOrder
    cryptomus = serializers.BooleanField(default=False, required=False, allow_null=True,)

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
        if select_booster:
            try :
                Booster.objects.get(booster_id = choose_booster, is_mobleg_player= True, can_choose_me= True)
            except Booster.DoesNotExist:
                raise serializers.ValidationError("Please select valid booster") 
            
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if data['select_booster'] == False  :
            data['choose_booster'] = 0
        return data   

    def validate_server(self, value):
        valid_servers = ["North America", "Europe", "SEA", "Asia"]
        if value not in valid_servers:
            raise serializers.ValidationError("Invalid server selection")
        return value


class PlacementSerializer(serializers.Serializer):
    last_rank           = serializers.IntegerField(min_value=0, max_value=11)
    number_of_match     = serializers.IntegerField(min_value=1, max_value=5)
    promo_code          = serializers.CharField()
    duo_boosting        = serializers.BooleanField()
    select_booster      = serializers.BooleanField()
    turbo_boost         = serializers.BooleanField()
    streaming           = serializers.BooleanField()
    server              = serializers.CharField()
    choose_booster      = serializers.IntegerField()

    # Order Info
    game_id = serializers.HiddenField(default=8)
    game_type = serializers.HiddenField(default='P')
    game_order_info = MOBLEG_POI
    order_model = MobileLegendsPlacementOrder
    cryptomus = serializers.BooleanField(default=False, required=False, allow_null=True,)

    def validate(self, attrs):
        self.booster_validate(attrs)
        return attrs

    def booster_validate(self, attrs):
        choose_booster = attrs.get('choose_booster', '')
        select_booster = attrs.get('select_booster', '')
        if select_booster:
            try :
                Booster.objects.get(booster_id = choose_booster, is_mobleg_player= True, can_choose_me= True)
            except Booster.DoesNotExist:
                raise serializers.ValidationError("Please select valid booster") 
            
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if data['select_booster'] == False  :
            data['choose_booster'] = 0
        return data   

    def validate_server(self, value):
        valid_servers = ["North America", "Europe", "SEA", "Asia"]
        if value not in valid_servers:
            raise serializers.ValidationError("Invalid server selection")
        return value
