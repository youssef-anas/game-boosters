from rest_framework import serializers
from booster.models import Booster
from accounts.models import BaseOrder
from ..models import HearthstoneDivisionOrder, HearthStoneBattleOrder
from .order_information import HS_DOI, HS_AOI

class DivisionSerializer(serializers.Serializer):
  current_rank        = serializers.IntegerField(min_value=1, max_value=5)
  current_division    = serializers.IntegerField(min_value=1, max_value=10)
  marks               = serializers.IntegerField(min_value=0, max_value=3)
  desired_rank        = serializers.IntegerField(min_value=1, max_value=6)
  desired_division    = serializers.IntegerField(min_value=1, max_value=10)
  duo_boosting        = serializers.BooleanField()
  select_booster      = serializers.BooleanField()
  turbo_boost         = serializers.BooleanField()
  streaming           = serializers.BooleanField()
  price               = serializers.FloatField(min_value=10)
  extend_order        = serializers.IntegerField()
  choose_booster      = serializers.IntegerField()
  promo_code          = serializers.CharField()
  server              = serializers.CharField()
  pass_extend = False

  # Order Info
  game_id = serializers.HiddenField(default=7)
  game_type = serializers.HiddenField(default='D')
  game_order_info = HS_DOI
  order_model = HearthstoneDivisionOrder
  cryptomus = serializers.BooleanField(default=False, required=False, allow_null=True,)

  def validate(self, attrs):
    self.extend_order_validate(attrs)
    if self.pass_extend == False:
      self.booster_validate(attrs)
    return attrs
    
  def extend_order_validate(self, attrs):
    extend_order = attrs.get('extend_order', '')
    if extend_order > 0:
        try:
            BaseOrder.objects.get(id=extend_order, game__id=7, game_type='D')
            self.pass_extend = True
        except BaseOrder.DoesNotExist:
            raise serializers.ValidationError("This order can't be extended")

          
  def booster_validate(self, attrs):
    choose_booster = attrs.get('choose_booster', '')
    select_booster = attrs.get('select_booster', '')
    if select_booster:
        try :
            Booster.objects.get(booster_id = choose_booster, is_hearthstone_player= True, can_choose_me= True)
        except Booster.DoesNotExist:
            raise serializers.ValidationError("Please select valid booster") 
        
  def validate_server(self, value):
    valid_servers = [
        "Americas", "Europe", "Asia", "China"
    ]
    if value not in valid_servers:
        raise serializers.ValidationError("Invalid server selection")
    return value               
        
  def to_internal_value(self, data):
    data = super().to_internal_value(data)
    if data['select_booster'] == False  :
        data['choose_booster'] = 0
    return data   
  

class BattleSerializer(serializers.Serializer):
  current_mmr    = serializers.IntegerField(min_value=0, max_value=10000)
  desired_mmr    = serializers.IntegerField(min_value=0, max_value=10000)
  duo_boosting        = serializers.BooleanField()
  select_booster      = serializers.BooleanField()
  turbo_boost         = serializers.BooleanField()
  streaming           = serializers.BooleanField()
  price               = serializers.FloatField(min_value=10)
  extend_order        = serializers.IntegerField()
  choose_booster      = serializers.IntegerField()
  promo_code          = serializers.CharField()
  server              = serializers.CharField()
  pass_extend = False


  # defaults
  current_rank = serializers.HiddenField(default=1)
  desired_rank = serializers.HiddenField(default=1)
  marks = serializers.HiddenField(default=0)


  # Order Info
  game_id = serializers.HiddenField(default=7)
  game_type = serializers.HiddenField(default='A')
  game_order_info = HS_AOI
  order_model = HearthStoneBattleOrder
  cryptomus = serializers.BooleanField(default=False, required=False, allow_null=True,)

  def validate(self, attrs):
    self.extend_order_validate(attrs)
    if self.pass_extend == False:
      self.booster_validate(attrs)
    return attrs
    
  def extend_order_validate(self, attrs):
    extend_order = attrs.get('extend_order', '')
    if extend_order > 0:
        try:
            BaseOrder.objects.get(id=extend_order, game__id=7, game_type='A')
            self.pass_extend = True
        except BaseOrder.DoesNotExist:
            raise serializers.ValidationError("This order can't be extended")

          
  def booster_validate(self, attrs):
    choose_booster = attrs.get('choose_booster', '')
    select_booster = attrs.get('select_booster', '')
    if select_booster:
        try :
            Booster.objects.get(booster_id = choose_booster, is_hearthstone_player= True, can_choose_me= True)
        except Booster.DoesNotExist:
            raise serializers.ValidationError("Please select valid booster") 
        
  def validate_server(self, value):
    valid_servers = [
        "Americas", "Europe", "Asia", "China"
    ]
    if value not in valid_servers:
        raise serializers.ValidationError("Invalid server selection")
    return value               
        
  def to_internal_value(self, data):
    data = super().to_internal_value(data)
    if data['select_booster'] == False  :
        data['choose_booster'] = 0
    return data   