from rest_framework import serializers
from accounts.models import BaseOrder
from booster.models import Booster

class ArenaSerializer(serializers.Serializer):
    current_rank = serializers.IntegerField(min_value=1, max_value=4)
    current_RP = serializers.IntegerField(min_value=0, max_value=2500)
    desired_rank = serializers.IntegerField(min_value=1, max_value=4)
    desired_RP = serializers.IntegerField(min_value=1, max_value=2500)
    is_arena_2vs2 = serializers.BooleanField()

    duo_boosting = serializers.BooleanField()
    select_booster = serializers.BooleanField()
    turbo_boost = serializers.BooleanField()
    streaming = serializers.BooleanField()

    server = serializers.CharField(max_length=300)
    price = serializers.FloatField(min_value=10)
    choose_booster = serializers.IntegerField()
    extend_order = serializers.IntegerField()
    promo_code = serializers.CharField()

    def validate(self, attrs):
        self.booster_validate(attrs)
        self.extend_order_validate(attrs)
        return attrs

    def booster_validate(self, attrs):
        choose_booster = attrs.get('choose_booster', '')
        select_booster = attrs.get('select_booster', '')
        if select_booster:
            try :
                Booster.objects.get(booster_id = choose_booster, is_wow_player= True, can_choose_me= True)
            except Booster.DoesNotExist:
                raise serializers.ValidationError("Please select valid booster")    
            
    def extend_order_validate(self, attrs):
        extend_order = attrs.get('extend_order', '')
        if extend_order > 0:
            try:
                BaseOrder.objects.get(id=extend_order, game__id=6, game_type='D')
            except BaseOrder.DoesNotExist:
                raise serializers.ValidationError("This order can't be extended")        

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if data['select_booster'] == False  :
            data['choose_booster'] = 0
        return data
    
    def validate_server(self, value):
        valid_servers = ["Europe", "US"]
        if value not in valid_servers:
            raise serializers.ValidationError("Invalid server selection")
        return value
    

class RaidSimpleSerializer(serializers.Serializer):
    WOW_MAP_CHOICES = (
        ("incarnates", "incarnates"),
        ("crucible", "crucible"),
        ("amirdrassil", "amirdrassil"),
    )
    map = serializers.ChoiceField(choices = WOW_MAP_CHOICES)
    bosses = serializers.CharField()
    difficulty_chosen = serializers.FloatField()

    duo_boosting = serializers.BooleanField()
    select_booster = serializers.BooleanField()
    turbo_boost = serializers.BooleanField()
    streaming = serializers.BooleanField()

    server = serializers.CharField(max_length=300)
    price = serializers.FloatField(min_value=10)
    choose_booster = serializers.IntegerField()
    promo_code = serializers.CharField()


    def validate(self, attrs):
        self.booster_validate(attrs)
        return attrs
    
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if data['select_booster'] == False  :
            data['choose_booster'] = 0
        return data
    
    def validate_server(self, value):
        valid_servers = ["EU", "US"]
        if value not in valid_servers:
            raise serializers.ValidationError("Invalid server selection")
        return value
    
    def booster_validate(self, attrs):
        choose_booster = attrs.get('choose_booster', '')
        select_booster = attrs.get('select_booster', '')
        if select_booster:
            try :
                Booster.objects.get(booster_id = choose_booster, is_wow_player= True, can_choose_me= True)
            except Booster.DoesNotExist:
                raise serializers.ValidationError("Please select valid booster")    
            


class RaidBundleSerializer(serializers.Serializer):
    bundle_id = serializers.CharField()
    difficulty_chosen = serializers.FloatField()

    duo_boosting = serializers.BooleanField()
    select_booster = serializers.BooleanField()
    turbo_boost = serializers.BooleanField()
    streaming = serializers.BooleanField()

    server = serializers.CharField(max_length=300)
    price = serializers.FloatField(min_value=10)
    choose_booster = serializers.IntegerField()
    promo_code = serializers.CharField()

    def validate(self, attrs):
        self.booster_validate(attrs)
        return attrs
    
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if data['select_booster'] == False  :
            data['choose_booster'] = 0
        return data
    
    def validate_server(self, value):
        valid_servers = ["EU", "US"]
        if value not in valid_servers:
            raise serializers.ValidationError("Invalid server selection")
        return value
    
    def booster_validate(self, attrs):
        choose_booster = attrs.get('choose_booster', '')
        select_booster = attrs.get('select_booster', '')
        if select_booster:
            try :
                Booster.objects.get(booster_id = choose_booster, is_wow_player= True, can_choose_me= True)
            except Booster.DoesNotExist:
                raise serializers.ValidationError("Please select valid booster")    

