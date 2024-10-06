from rest_framework import serializers
from accounts.models import BaseOrder
from booster.models import Booster
from ..models import RocketLeagueDivisionOrder, RocketLeaguePlacementOrder, RocketLeagueTournamentOrder, RocketLeagueSeasonalOrder
from .order_information import RL_DOI, RL_SOI, RL_POI, RL_TOI

class DivisionSerializer(serializers.Serializer):
    ranked_type         = serializers.IntegerField(min_value=1, max_value=3)
    
    current_rank        = serializers.IntegerField(min_value=1, max_value=7)
    current_division    = serializers.IntegerField(min_value=1, max_value=3)
    desired_rank        = serializers.IntegerField(min_value=1, max_value=8)
    desired_division    = serializers.IntegerField(min_value=1, max_value=3)
    marks = serializers.HiddenField(default=0)

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
    game_id = serializers.HiddenField(default=9)
    game_type = serializers.HiddenField(default='D')
    game_order_info = RL_DOI
    order_model = RocketLeagueDivisionOrder
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
                Booster.objects.get(booster_id = choose_booster, is_rl_player= True, can_choose_me= True)
            except Booster.DoesNotExist:
                raise serializers.ValidationError("Please select valid booster")  
            
    def extend_order_validate(self, attrs):
        extend_order = attrs.get('extend_order', '')
        if extend_order > 0:
            try:
                BaseOrder.objects.get(id=extend_order, game__id=9, game_type='D')
            except BaseOrder.DoesNotExist:
                raise serializers.ValidationError("This order can't be extended")        

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if data['select_booster'] == False  :
            data['choose_booster'] = 0
        return data

    def validate_server(self, value):
        valid_servers = [
            "North America", "Europe", "Brazil", "Asia Pacific",
            "Middle East", "Oceania", "Japan"
        ]
        if value not in valid_servers:
            raise serializers.ValidationError("Invalid server selection")
        return value

class PlacementSerializer(serializers.Serializer):
  last_rank           = serializers.IntegerField(min_value=1, max_value=8)
  number_of_match     = serializers.IntegerField(min_value=1, max_value=10)

  duo_boosting        = serializers.BooleanField()
  select_booster      = serializers.BooleanField()
  turbo_boost         = serializers.BooleanField()
  streaming           = serializers.BooleanField()

  server              = serializers.CharField(max_length=300)
  price               = serializers.FloatField(min_value=10)
  choose_booster      = serializers.IntegerField()
  # extend_order        = serializers.IntegerField()
  promo_code          = serializers.CharField()

  # Order Info
  game_id = serializers.HiddenField(default=9)
  game_type = serializers.HiddenField(default='P')
  game_order_info = RL_POI
  order_model = RocketLeaguePlacementOrder
  cryptomus = serializers.BooleanField(default=False, required=False, allow_null=True,)

  def validate(self, attrs):
      self.booster_validate(attrs)
      return attrs

  def booster_validate(self, attrs):
      choose_booster = attrs.get('choose_booster', '')
      select_booster = attrs.get('select_booster', '')
      if select_booster:
          try :
              Booster.objects.get(booster_id = choose_booster, is_pubg_player= True, can_choose_me= True)
          except Booster.DoesNotExist:
              raise serializers.ValidationError("Please select valid booster")      
          

  def validate_server(self, value):
    valid_servers = [
        "North America", "Europe", "Brazil", "Asia Pacific",
        "Middle East", "Oceania", "Japan"
    ]
    if value not in valid_servers:
        raise serializers.ValidationError("Invalid server selection")
    return value        

  def to_internal_value(self, data):
      data = super().to_internal_value(data)
      if data['select_booster'] == False  :
          data['choose_booster'] = 0
      return data

  def validate_server(self, value):
    valid_servers = [
        "North America", "Europe", "Brazil", "Asia Pacific",
        "Middle East", "Oceania", "Japan"
    ]
    if value not in valid_servers:
        raise serializers.ValidationError("Invalid server selection")
    return value

class SeasonalSerializer(serializers.Serializer):
  current_rank        = serializers.IntegerField(min_value=1, max_value=8)
  number_of_wins      = serializers.IntegerField(min_value=1, max_value=5)

  duo_boosting        = serializers.BooleanField()
  select_booster      = serializers.BooleanField()
  turbo_boost         = serializers.BooleanField()
  streaming           = serializers.BooleanField()

  server              = serializers.CharField(max_length=300)
  price               = serializers.FloatField(min_value=10)
  choose_booster      = serializers.IntegerField()
  # extend_order        = serializers.IntegerField()
  promo_code          = serializers.CharField()

  # Order Info
  game_id = serializers.HiddenField(default=9)
  game_type = serializers.HiddenField(default='S')
  game_order_info = RL_SOI
  order_model = RocketLeagueSeasonalOrder
  cryptomus = serializers.BooleanField(default=False, required=False, allow_null=True,)

  def validate(self, attrs):
      self.booster_validate(attrs)
      return attrs
  
  def validate_server(self, value):
    valid_servers = [
        "North America", "Europe", "Brazil", "Asia Pacific",
        "Middle East", "Oceania", "Japan"
    ]
    if value not in valid_servers:
        raise serializers.ValidationError("Invalid server selection")
    return value      

  def booster_validate(self, attrs):
      choose_booster = attrs.get('choose_booster', '')
      select_booster = attrs.get('select_booster', '')
      if select_booster:
          try :
              Booster.objects.get(booster_id = choose_booster, is_pubg_player= True, can_choose_me= True)
          except Booster.DoesNotExist:
              raise serializers.ValidationError("Please select valid booster")        

  def to_internal_value(self, data):
      data = super().to_internal_value(data)
      if data['select_booster'] == False  :
          data['choose_booster'] = 0
      return data

  def validate_server(self, value):
    valid_servers = [
        "North America", "Europe", "Brazil", "Asia Pacific",
        "Middle East", "Oceania", "Japan"
    ]
    if value not in valid_servers:
        raise serializers.ValidationError("Invalid server selection")
    return value

class TournamentSerializer(serializers.Serializer):
  current_league      = serializers.IntegerField(min_value=1, max_value=8)

  duo_boosting        = serializers.BooleanField()
  select_booster      = serializers.BooleanField()
  turbo_boost         = serializers.BooleanField()
  streaming           = serializers.BooleanField()

  server              = serializers.CharField(max_length=300)
  price               = serializers.FloatField(min_value=10)
  choose_booster      = serializers.IntegerField()
  # extend_order        = serializers.IntegerField()
  promo_code          = serializers.CharField()

  # Order Info
  game_id = serializers.HiddenField(default=9)
  game_type = serializers.HiddenField(default='T')
  game_order_info = RL_TOI
  order_model = RocketLeagueTournamentOrder
  cryptomus = serializers.BooleanField(default=False, required=False, allow_null=True,)

  def validate(self, attrs):
      self.booster_validate(attrs)
      return attrs
  
  def validate_server(self, value):
    valid_servers = [
        "North America", "Europe", "Brazil", "Asia Pacific",
        "Middle East", "Oceania", "Japan"
    ]
    if value not in valid_servers:
        raise serializers.ValidationError("Invalid server selection")
    return value      

  def booster_validate(self, attrs):
      choose_booster = attrs.get('choose_booster', '')
      select_booster = attrs.get('select_booster', '')
      if select_booster:
          try :
              Booster.objects.get(booster_id = choose_booster, is_pubg_player= True, can_choose_me= True)
          except Booster.DoesNotExist:
              raise serializers.ValidationError("Please select valid booster")       

  def to_internal_value(self, data):
      data = super().to_internal_value(data)
      if data['select_booster'] == False  :
          data['choose_booster'] = 0
      return data
  
  def validate_server(self, value):
    valid_servers = [
        "North America", "Europe", "Brazil", "Asia Pacific",
        "Middle East", "Oceania", "Japan"
    ]
    if value not in valid_servers:
        raise serializers.ValidationError("Invalid server selection")
    return value