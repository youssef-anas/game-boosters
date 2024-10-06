from rest_framework import serializers
from accounts.models import BaseOrder
from booster.models import Booster
from ..models import Dota2PlacementOrder, Dota2RankBoostOrder
from .order_information import Dota2_AOI, Dota2_POI


class RankBoostSerializer(serializers.Serializer):

    current_rank        = serializers.IntegerField(min_value=1, max_value=8)
    desired_rank        = serializers.IntegerField(min_value=1, max_value=8)
    current_division    = serializers.IntegerField(min_value=0, max_value=8000)
    desired_division    = serializers.IntegerField(min_value=500, max_value=8000)
    role                = serializers.IntegerField(min_value=1, max_value=2)
    duo_boosting        = serializers.BooleanField()
    select_booster      = serializers.BooleanField()
    turbo_boost         = serializers.BooleanField()
    streaming           = serializers.BooleanField()
    server              = serializers.CharField(max_length=300)
    price               = serializers.FloatField(min_value=10)
    choose_booster      = serializers.IntegerField()
    extend_order        = serializers.IntegerField()
    promo_code          = serializers.CharField()

    marks = serializers.HiddenField(default=0)

    # Order Info
    game_id = serializers.HiddenField(default=10)
    game_type = serializers.HiddenField(default='A')
    game_order_info = Dota2_AOI
    order_model = Dota2RankBoostOrder
    cryptomus = serializers.BooleanField(default=False, required=False, allow_null=True,)

    def validate(self, attrs):
        self.extend_order_validate(attrs)
        self.booster_validate(attrs)
        return attrs
    
    def extend_order_validate(self, attrs):
        extend_order = attrs.get('extend_order', '')
        if extend_order > 0:
            try:
                BaseOrder.objects.get(id=extend_order, game__id=10, game_type='A')
            except BaseOrder.DoesNotExist:
                raise serializers.ValidationError("This order can't be extended")
  
            
    def booster_validate(self, attrs):
        choose_booster = attrs.get('choose_booster', '')
        select_booster = attrs.get('select_booster', '')
        if select_booster:
            try :
                Booster.objects.get(booster_id = choose_booster, is_dota2_player= True, can_choose_me= True)
            except Booster.DoesNotExist:
                raise serializers.ValidationError("Please select valid booster") 
            
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if data['select_booster'] == False  :
            data['choose_booster'] = 0
        return data   
    
    def validate_server(self, value):
        valid_servers = ["US West", "US East", "EU West", "EU East", "Asia", "South America", "Russia", "South Africa", "OCE"]
        if value not in valid_servers:
            raise serializers.ValidationError("Invalid server selection")
        return value


class PlacementSerializer(serializers.Serializer):
    last_rank           = serializers.IntegerField(min_value=1, max_value=8)
    last_division       = serializers.IntegerField(min_value=0, max_value=8000)
    number_of_match     = serializers.IntegerField(min_value=1, max_value=10)
    role                = serializers.IntegerField(min_value=1, max_value=2)
    duo_boosting        = serializers.BooleanField()
    select_booster      = serializers.BooleanField()
    turbo_boost         = serializers.BooleanField()
    streaming           = serializers.BooleanField()
    server              = serializers.CharField(max_length=300)
    price               = serializers.FloatField(min_value=10)
    choose_booster      = serializers.IntegerField()
    extend_order        = serializers.IntegerField()
    promo_code          = serializers.CharField()

    # Order Info
    game_id = serializers.HiddenField(default=10)
    game_type = serializers.HiddenField(default='P')
    game_order_info = Dota2_POI
    order_model = Dota2PlacementOrder
    cryptomus = serializers.BooleanField(default=False, required=False, allow_null=True,)

    def validate(self, attrs):
        self.extend_order_validate(attrs)
        self.booster_validate(attrs)
        return attrs
    
    def extend_order_validate(self, attrs):
        extend_order = attrs.get('extend_order', '')
        if extend_order > 0:
            try:
                BaseOrder.objects.get(id=extend_order, game__id=10, game_type='P')
            except BaseOrder.DoesNotExist:
                raise serializers.ValidationError("This order can't be extended")
  
            
    def booster_validate(self, attrs):
        choose_booster = attrs.get('choose_booster', '')
        select_booster = attrs.get('select_booster', '')
        if select_booster:
            try :
                Booster.objects.get(booster_id = choose_booster, is_dota2_player= True, can_choose_me= True)
            except Booster.DoesNotExist:
                raise serializers.ValidationError("Please select valid booster") 
            
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if data['select_booster'] == False  :
            data['choose_booster'] = 0
        return data   
    
    def validate_server(self, value):
        valid_servers = ["US West", "US East", "EU West", "EU East", "Asia", "South America", "Russia", "South Africa", "OCE"]
        if value not in valid_servers:
            raise serializers.ValidationError("Invalid server selection")
        return value
