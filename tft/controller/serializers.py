from rest_framework import serializers
from accounts.models import BaseOrder
from booster.models import Booster
from ..models import TFTDivisionOrder, TFTPlacementOrder
from .order_information import TFT_DOI, TFT_POI

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

    # Order Info
    game_id = serializers.HiddenField(default=5)
    game_type = serializers.HiddenField(default='D')
    game_order_info = TFT_DOI
    order_model = TFTDivisionOrder
    cryptomus = serializers.BooleanField(default=False, required=False, allow_null=True,)

    def validate(self, attrs):
        self.booster_validate(attrs)
        self.extend_order_validate(attrs)
        return attrs

    def booster_validate(self, attrs):
        choose_booster = attrs.get('choose_booster', '')
        select_booster = attrs.get('select_booster', '')
        if select_booster:
            try :
                Booster.objects.get(booster_id = choose_booster, is_tft_player= True, can_choose_me= True)
            except Booster.DoesNotExist:
                raise serializers.ValidationError("Please select valid booster")      
            
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

    def validate_server(self, value):
        valid_servers = [
            "North America", "Europe West", "Europe East", "Brazil",
            "Latin Amer Nor", "Latin Amer Sou", "Oceania", "Japan",
            "Russia", "Turkey", "Vietnam", "Garena SEA"
        ]
        if value not in valid_servers:
            raise serializers.ValidationError("Invalid server selection")
        return value


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


    # Order Info
    game_id = serializers.HiddenField(default=5)
    game_type = serializers.HiddenField(default='D')
    game_order_info = TFT_POI
    order_model = TFTPlacementOrder
    cryptomus = serializers.BooleanField(default=False, required=False, allow_null=True,)

    def validate(self, attrs):
        self.booster_validate(attrs)
        return attrs

    def booster_validate(self, attrs):
        choose_booster = attrs.get('choose_booster', '')
        select_booster = attrs.get('select_booster', '')
        if select_booster:
            try :
                Booster.objects.get(booster_id = choose_booster, is_tft_player= True, can_choose_me= True)
            except Booster.DoesNotExist:
                raise serializers.ValidationError("Please select valid booster")     

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if data['select_booster'] == False  :
            data['choose_booster'] = 0
        return data
    
    def validate_server(self, value):
        valid_servers = [
            "North America", "Europe West", "Europe East", "Brazil",
            "Latin Amer Nor", "Latin Amer Sou", "Oceania", "Japan",
            "Russia", "Turkey", "Vietnam", "Garena SEA"
        ]
        if value not in valid_servers:
            raise serializers.ValidationError("Invalid server selection")
        return value