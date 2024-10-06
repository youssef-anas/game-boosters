from rest_framework import serializers
from accounts.models import BaseOrder
from customer.models import Champion
from booster.models import Booster
from wildRift.validators import validate_marks_for_rank, validate_master_division
from .order_information import WildRiftDivisionOrderInfo
from wildRift.models import WildRiftDivisionOrder


class RankSerializer(serializers.Serializer):
    current_rank = serializers.IntegerField(min_value=1, max_value=7)
    current_division = serializers.IntegerField(min_value=1, max_value=4)

    marks = serializers.IntegerField(min_value=0, max_value=5)
    
    desired_rank = serializers.IntegerField(min_value=1, max_value=8)
    desired_division = serializers.IntegerField(min_value=1, max_value=4)

    server = serializers.CharField(max_length=300)

    duo_boosting = serializers.BooleanField()
    select_booster = serializers.BooleanField()
    turbo_boost = serializers.BooleanField()
    streaming = serializers.BooleanField()
    select_champion = serializers.BooleanField()

    price = serializers.FloatField(min_value=0)

    choose_booster = serializers.IntegerField()
    champion_data = serializers.CharField(allow_blank=True)

    extend_order = serializers.IntegerField()

    promo_code = serializers.CharField()


    # Order Info
    game_id = serializers.HiddenField(default=1)
    game_type = serializers.HiddenField(default='D')
    game_order_info = WildRiftDivisionOrderInfo
    order_model = WildRiftDivisionOrder
    cryptomus = serializers.BooleanField(default=False, required=False, allow_null=True,)

    def validate(self, attrs):
        pass_validate = False
        current_rank_id = attrs.get('current_rank')
        current_marks = attrs.get('marks')
        desired_rank_id = attrs.get('desired_rank')

        # Validate current_marks
        validate_marks_for_rank(current_rank_id, current_marks)
        validate_marks_for_rank(desired_rank_id, 0)

        # Validate desired_rank
        if desired_rank_id == 8:  # MASTER
            desired_division = attrs.get('desired_division')
            validate_master_division(desired_division)

        pass_validate = self.extend_order_validate(attrs)
        if not pass_validate:
            self.booster_validate(attrs)
            self.champion_validate(attrs)
        return attrs
    
    def extend_order_validate(self, attrs):
        extend_order = attrs.get('extend_order', '')
        if extend_order > 0:
            try:
                BaseOrder.objects.get(id=extend_order, game__id=1, game_type='D')
                return True
            except BaseOrder.DoesNotExist:
                raise serializers.ValidationError("This order can't be extended")
  
            
    def booster_validate(self, attrs):
        choose_booster = attrs.get('choose_booster', None)
        select_booster = attrs.get('select_booster', None)
        if select_booster:
            try :
                Booster.objects.get(booster_id = choose_booster, is_wr_player= True, can_choose_me= True)
            except Booster.DoesNotExist:
                raise serializers.ValidationError("Please select valid booster")
            
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if data['select_booster'] == False  :
            data['choose_booster'] = 0
        if data['select_champion'] == False:
            data['champion_data'] = []
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
                        Champion.objects.get(id=id, game__id = 1)
                    except Champion.DoesNotExist:
                        raise serializers.ValidationError("This champion is not belong to Wild Rift.")
            attrs['champion_data'] = numbers_list        
            return attrs

    def validate_server(self, value):
        valid_servers = [
            "North America", "Europe West", "Brazil", "Oceania",
            "Japan", "Russia", "Middle East", "Asia Pacific"
        ]
        if value not in valid_servers:
            raise serializers.ValidationError("Invalid server selection")
        return value