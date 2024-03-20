from rest_framework import serializers
from accounts.models import BaseOrder
from valorant.models import ValorantDivisionOrder
from customer.models import Champion
from booster.models import Booster

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

    def validate(self, attrs):
        self.extend_order_validate(attrs)
        self.booster_validate(attrs)
        self.champion_validate(attrs)
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
                Booster.objects.get(booster_id = choose_booster, is_valo_player= True, can_choose_me= True)
            except Booster.DoesNotExist:
                raise serializers.ValidationError("This Booster is not belong to Valorent.")
            
    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        if data['choose_booster'] and data['select_booster'] :
            data['choose_booster'] = 0
        return data           

    
    def champion_validate(self, attrs):
            champion_data = attrs.get('champion_data', '')
            select_champion = attrs.get('select_champion', '')
            if champion_data and champion_data != 'null' and select_champion:
                print(champion_data)
                try :
                    numbers_list = [int(num) for num in champion_data.split("ch") if num]
                    if len(numbers_list) > 3:
                        raise serializers.ValidationError("3 champion IDs only can be selected.")
                    for id in numbers_list:
                        try:
                            Champion.objects.get(id=id, game__id = 2)
                        except Champion.DoesNotExist:
                            raise serializers.ValidationError("This champion is not belong to Valorent.")
                except:
                    raise serializers.ValidationError("Error, when try to set champions.") 


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

    extend_order = serializers.IntegerField()

    promo_code = serializers.CharField()