from rest_framework import serializers
from accounts.models import BaseOrder
from booster.models import Booster
from .order_information import Csgo2_DOI, Csgo2_AOI, Csgo2_FOI
from ..models import CsgoFaceitOrder, Csgo2PremierOrder, Csgo2DivisionOrder

class DivisionSerializer(serializers.Serializer):
    current_rank = serializers.IntegerField(min_value=1, max_value=17)
    desired_rank = serializers.IntegerField(min_value=1, max_value=18)
    server = serializers.CharField(max_length=300)
    promo_code = serializers.CharField()

    duo_boosting = serializers.BooleanField()
    select_booster = serializers.BooleanField()
    turbo_boost = serializers.BooleanField()
    streaming = serializers.BooleanField()
    price = serializers.FloatField(min_value=10)
    choose_booster = serializers.IntegerField()
    extend_order = serializers.IntegerField()

    # 
    current_division = serializers.HiddenField(default=1)
    desired_division = serializers.HiddenField(default=1)
    marks = serializers.HiddenField(default=0)

    # Order Info
    game_id = serializers.HiddenField(default=13)
    game_type = serializers.HiddenField(default='D')
    game_order_info = Csgo2_DOI
    order_model = Csgo2DivisionOrder
    cryptomus = serializers.BooleanField(default=False, required=False, allow_null=True,)

    
    

    def validate(self, attrs):
        pass_validate = False

        pass_validate = self.extend_order_validate(attrs)
        if not pass_validate:
            self.booster_validate(attrs)
        return attrs
    
    def extend_order_validate(self, attrs):
        extend_order = attrs.get('extend_order', '')
        if extend_order > 0:
            try:
                BaseOrder.objects.get(id=extend_order, game__id=13, game_type='D')
                return True
            except BaseOrder.DoesNotExist:
                raise serializers.ValidationError("This order can't be extended")
  
            
    def booster_validate(self, attrs):
        choose_booster = attrs.get('choose_booster', None)
        select_booster = attrs.get('select_booster', None)
        if select_booster:
            try :
                Booster.objects.get(booster_id = choose_booster, is_csgo2_player= True, can_choose_me= True)
            except Booster.DoesNotExist:
                raise serializers.ValidationError("Please select valid booster") 
            
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if data['select_booster'] == False  :
            data['choose_booster'] = 0
        return data            
    
class FaceitSerializer(serializers.Serializer):
    current_level = serializers.IntegerField(min_value=1, max_value=10)
    desired_level = serializers.IntegerField(min_value=1, max_value=10)

    duo_boosting = serializers.BooleanField()
    select_booster = serializers.BooleanField()
    turbo_boost = serializers.BooleanField()
    streaming = serializers.BooleanField()

    server = serializers.CharField(max_length=300)
    price = serializers.FloatField(min_value=10)

    choose_booster = serializers.IntegerField()
    promo_code = serializers.CharField()

    # Order Info
    game_id = serializers.HiddenField(default=13)
    game_type = serializers.HiddenField(default='A')
    game_order_info = Csgo2_FOI
    order_model = CsgoFaceitOrder
    cryptomus = serializers.BooleanField(default=False, required=False, allow_null=True,)



    def validate(self, attrs):
        self.booster_validate(attrs)
        return attrs
            
    def booster_validate(self, attrs):
        choose_booster = attrs.get('choose_booster', None)
        select_booster = attrs.get('select_booster', None)
        if select_booster:
            try :
                Booster.objects.get(booster_id = choose_booster, is_csgo2_player= True, can_choose_me= True)
            except Booster.DoesNotExist:
                raise serializers.ValidationError("Please select valid booster") 
            
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if data['select_booster'] == False  :
            data['choose_booster'] = 0
        return data      


    
class PremierSerializer(serializers.Serializer):

    current_rank = serializers.IntegerField(min_value=1, max_value=8)
    desired_rank = serializers.IntegerField(min_value=1, max_value=8)
    # division
    current_division = serializers.IntegerField(min_value=0, max_value=29500)
    desired_division = serializers.IntegerField(min_value=500, max_value=30000)

    # exra filds about order
    duo_boosting = serializers.BooleanField()
    select_booster = serializers.BooleanField()
    turbo_boost = serializers.BooleanField()
    streaming = serializers.BooleanField()

    server = serializers.CharField(max_length=300)
    price = serializers.FloatField(min_value=10)

    choose_booster = serializers.IntegerField()
    promo_code = serializers.CharField()
    extend_order = serializers.IntegerField()

    # 
    marks = serializers.HiddenField(default=0)

    # Order Info
    game_id = serializers.HiddenField(default=13)
    game_type = serializers.HiddenField(default='A')
    game_order_info = Csgo2_AOI
    order_model = Csgo2PremierOrder 
    cryptomus = serializers.BooleanField(default=False, required=False, allow_null=True,)

    def validate(self, attrs):
        self.extend_order_validate(attrs)
        self.booster_validate(attrs)
        return attrs
    
    def extend_order_validate(self, attrs):
        extend_order = attrs.get('extend_order', '')
        if extend_order > 0:
            try:
                BaseOrder.objects.get(id=extend_order, game__id=13, game_type='A')
            except BaseOrder.DoesNotExist:
                raise serializers.ValidationError("This order can't be extended")
  
            
    def booster_validate(self, attrs):
        choose_booster = attrs.get('choose_booster', None)
        select_booster = attrs.get('select_booster', None)
        if select_booster:
            try :
                Booster.objects.get(booster_id = choose_booster, is_csgo2_player= True, can_choose_me= True)
            except Booster.DoesNotExist:
                raise serializers.ValidationError("Please select valid booster") 
            
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if data['select_booster'] == False  :
            data['choose_booster'] = 0
        return data   