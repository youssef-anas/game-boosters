from rest_framework import serializers
from accounts.models import BaseOrder
from booster.models import Booster
from .order_information import OverWatch_DOI, OverWatch_POI
from ..models import Overwatch2DivisionOrder, Overwatch2PlacementOrder

class DivisionSerializer(serializers.Serializer):
    current_rank        = serializers.IntegerField(min_value=1, max_value=8)
    current_division    = serializers.IntegerField(min_value=1, max_value=5)
    marks               = serializers.IntegerField(min_value=0, max_value=5)
    desired_rank        = serializers.IntegerField(min_value=1, max_value=8)
    desired_division    = serializers.IntegerField(min_value=1, max_value=5)

    duo_boosting        = serializers.BooleanField()
    select_booster      = serializers.BooleanField()
    streaming           = serializers.BooleanField()
    turbo_boost         = serializers.BooleanField()

    price               = serializers.FloatField(min_value=10)
    choose_booster      = serializers.IntegerField()
    
    extend_order        = serializers.IntegerField()
    promo_code          = serializers.CharField()
    server              = serializers.CharField()
    role                = serializers.IntegerField()

    # Order Info
    game_id = serializers.HiddenField(default=12)
    game_type = serializers.HiddenField(default='D')
    cryptomus = serializers.BooleanField(default=False, required=False, allow_null=True,)
    game_order_info = OverWatch_DOI
    order_model = Overwatch2DivisionOrder

    def validate(self, attrs):
        pass_validate = False
        pass_validate =  self.extend_order_validate(attrs)
        if not pass_validate:
            self.booster_validate(attrs)
            self.validate_server_overwatch(attrs.get('server'))
        return attrs
        
    def extend_order_validate(self, attrs):
        extend_order = attrs.get('extend_order', '')
        if extend_order > 0:
            try:
                BaseOrder.objects.get(id=extend_order, game__id=12, game_type='D')
                return True
            except BaseOrder.DoesNotExist:
                raise serializers.ValidationError("This order can't be extended")
            
    def validate_role(self, value):
        if value not in [1,2,3]:
            raise serializers.ValidationError("Role must be 1, 2, or 3.")
        return value        

            
    def booster_validate(self, attrs):
        choose_booster = attrs.get('choose_booster', '')
        select_booster = attrs.get('select_booster', '')
        if select_booster:
            try :
                Booster.objects.get(booster_id = choose_booster, is_overwatch2_player= True, can_choose_me= True)
            except Booster.DoesNotExist:
                raise serializers.ValidationError("Please select valid booster") 
            
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if data['select_booster'] == False  :
            data['choose_booster'] = 0
        return data   

    def validate_server_overwatch(self, value):
        valid_servers = [
            "North America", "Europe", "Brazil", "Asia Pacific"
        ]
        if value not in valid_servers:
            raise serializers.ValidationError("Invalid server selection")
        return value

class PlacementSerializer(serializers.Serializer):
    last_rank           = serializers.IntegerField(min_value=0, max_value=9)
    number_of_match     = serializers.IntegerField(min_value=1, max_value=5)

    duo_boosting        = serializers.BooleanField()
    select_booster      = serializers.BooleanField()
    streaming           = serializers.BooleanField()
    turbo_boost         = serializers.BooleanField()

    price               = serializers.FloatField(min_value=10)
    choose_booster      = serializers.IntegerField()

    promo_code          = serializers.CharField()
    server              = serializers.CharField()
    # role                = serializers.IntegerField()

    # Order Info
    game_id = serializers.HiddenField(default=12)
    game_type = serializers.HiddenField(default='P')
    game_order_info = OverWatch_POI
    cryptomus = serializers.BooleanField(default=False, required=False, allow_null=True,)
    order_model = Overwatch2PlacementOrder

    def validate(self, attrs):
        self.booster_validate(attrs)
        return attrs

    def booster_validate(self, attrs):
        choose_booster = attrs.get('choose_booster', '')
        select_booster = attrs.get('select_booster', '')
        if select_booster:
            try :
                Booster.objects.get(booster_id = choose_booster, is_overwatch2_player= True, can_choose_me= True)
            except Booster.DoesNotExist:
                raise serializers.ValidationError("Please select valid booster") 

    # def validate_role(self, value):
    #     if value not in [1,2,3]:
    #         raise serializers.ValidationError("Role must be 1, 2, or 3.")
    #     return value        

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if data['select_booster'] == False  :
            data['choose_booster'] = 0
        return data   


    def validate_server(self, value):
        valid_servers = [
            "North America", "Europe", "Brazil", "Asia Pacific"
        ]
        if value not in valid_servers:
            raise serializers.ValidationError("Invalid server selection")
        return value