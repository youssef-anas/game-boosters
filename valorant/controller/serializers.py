from rest_framework import serializers
from accounts.models import BaseOrder
from customer.models import Champion
from booster.models import Booster
from .order_information import ValorantDOI, VlorantPOI
from valorant.models import ValorantDivisionOrder, ValorantPlacementOrder

class DivisionSerializer(serializers.Serializer):
    current_rank = serializers.IntegerField(min_value=1, max_value=8)
    current_division = serializers.IntegerField(min_value=1, max_value=3)
    marks = serializers.IntegerField(min_value=0, max_value=4)
    desired_rank = serializers.IntegerField(min_value=1, max_value=8)
    desired_division = serializers.IntegerField(min_value=1, max_value=3)

    duo_boosting = serializers.BooleanField()
    select_booster = serializers.BooleanField()
    turbo_boost = serializers.BooleanField()
    streaming = serializers.BooleanField()
    select_champion = serializers.BooleanField()
    champion_data = serializers.CharField(allow_blank=True)

    server = serializers.CharField(max_length=300)
    price = serializers.FloatField(min_value=10)
    choose_booster = serializers.IntegerField()
    extend_order = serializers.IntegerField()
    promo_code = serializers.CharField(allow_blank=True)

    # Order Info
    game_id = serializers.HiddenField(default=2)
    game_type = serializers.HiddenField(default='D')
    game_order_info = ValorantDOI
    order_model = ValorantDivisionOrder
    cryptomus = serializers.BooleanField(default=False, required=False, allow_null=True,)

    def validate(self, attrs):
        self.extend_order_validate(attrs)
        self.booster_validate(attrs)
        self.champion_validate(attrs)
        return attrs
    
    def extend_order_validate(self, attrs):
        extend_order = attrs.get('extend_order', 0)
        if extend_order > 0:
            try:
                BaseOrder.objects.get(id=extend_order, game__id=2, game_type='D')
            except BaseOrder.DoesNotExist:
                raise serializers.ValidationError("This order can't be extended")
  
            
    def booster_validate(self, attrs):
        choose_booster = attrs.get('choose_booster', '')
        select_booster = attrs.get('select_booster', '')
        print(select_booster)
        if select_booster:
            try :
                Booster.objects.get(booster_id = choose_booster, is_valo_player= True, can_choose_me= True)
            except Booster.DoesNotExist:
                raise serializers.ValidationError("Please select valid booster")    
            
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if data['select_booster'] == False  :
            data['choose_booster'] = 0
        if data['select_champion'] == False:
            data['champion_data'] = 0
        return data                

    
    def champion_validate(self, attrs):
            champion_data = attrs.get('champion_data', None)
            select_champion = attrs.get('select_champion', None)
            numbers_list = []
            if champion_data and champion_data != 'null' and select_champion:
                try:
                    numbers_list = [int(num) for num in champion_data.split("ch") if num]
                except ValueError:
                    raise serializers.ValidationError("Error in champions")
                if len(numbers_list) > 3:
                    raise serializers.ValidationError("You can choose max 3 champions.")
                for id in numbers_list:
                    try:
                        Champion.objects.get(id=id, game__id = 2)
                    except Champion.DoesNotExist:
                        raise serializers.ValidationError("This champion is not belong to Valorent.")
            attrs['champion_data'] = numbers_list        
            return attrs    
                    
    def validate_server(self, value):
        valid_servers = ["North America", "Europe", "Asia Pacific"]
        if value not in valid_servers:
            raise serializers.ValidationError("Invalid server selection")
        return value                    
                    

class PlacementSerializer(serializers.Serializer):
    last_rank = serializers.IntegerField(min_value=0, max_value=8)
    number_of_match = serializers.IntegerField(min_value=1, max_value=5)

    duo_boosting = serializers.BooleanField()
    select_booster = serializers.BooleanField()
    turbo_boost = serializers.BooleanField()
    streaming = serializers.BooleanField()
    select_champion = serializers.BooleanField()

    server = serializers.CharField(max_length=300)
    price = serializers.FloatField(min_value=10)

    choose_booster = serializers.IntegerField()
    champion_data = serializers.CharField(allow_blank=True)
    promo_code = serializers.CharField()

        # Order Info
    game_id = serializers.HiddenField(default=2)
    game_type = serializers.HiddenField(default='P')
    game_order_info = VlorantPOI
    order_model = ValorantPlacementOrder
    cryptomus = serializers.BooleanField(default=False, required=False, allow_null=True,)

    def validate(self, attrs):
        self.extend_order_validate(attrs)
        self.booster_validate(attrs)
        self.champion_validate(attrs)
        return attrs
    
    def extend_order_validate(self, attrs):
        extend_order = attrs.get('extend_order', 0)
        if extend_order > 0:
            try:
                BaseOrder.objects.get(id=extend_order, game__id=2, game_type='P')
            except BaseOrder.DoesNotExist:
                raise serializers.ValidationError("This order can't be extended")
  
            
    def booster_validate(self, attrs):
        choose_booster = attrs.get('choose_booster', None)
        select_booster = attrs.get('select_booster', None)
        if select_booster:
            try :
                Booster.objects.get(booster_id = choose_booster, is_valo_player= True, can_choose_me= True)
            except Booster.DoesNotExist:
                raise serializers.ValidationError("Please select valid booster")    
            
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if data['select_booster'] == False  :
            data['choose_booster'] = 0
        if data['select_champion'] == False:
            data['champion_data'] = 0
        return data                

    
    def champion_validate(self, attrs):
            champion_data = attrs.get('champion_data', None)
            select_champion = attrs.get('select_champion', None)
            numbers_list = []
            if champion_data and champion_data != 'null' and select_champion:
                numbers_list = None
                try:
                    numbers_list = [int(num) for num in champion_data.split("ch") if num]
                except ValueError:
                    raise serializers.ValidationError("Error in champions")
                if len(numbers_list) > 3:
                    raise serializers.ValidationError("You can choose max 3 champions.")
                for id in numbers_list:
                    try:
                        Champion.objects.get(id=id, game__id = 2)
                    except Champion.DoesNotExist:
                        raise serializers.ValidationError("This champion is not belong to Valorent.")
            attrs['champion_data'] = numbers_list        
            return attrs        

    def validate_server(self, value):
        valid_servers = ["North America", "Europe", "Asia Pacific"]
        if value not in valid_servers:
            raise serializers.ValidationError("Invalid server selection")
        return value                    