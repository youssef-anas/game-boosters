from rest_framework import serializers
from accounts.models import BaseOrder
from booster.models import Booster
from .order_information import PubgDOI
from pubg.models import PubgDivisionOrder

class DivisionSerializer(serializers.Serializer):
    current_rank        = serializers.IntegerField(min_value=1, max_value=10)
    current_division    = serializers.IntegerField(min_value=1, max_value=5)
    marks               = serializers.IntegerField(min_value=0, max_value=4)
    desired_rank        = serializers.IntegerField(min_value=1, max_value=10)
    desired_division    = serializers.IntegerField(min_value=1, max_value=5)

    duo_boosting        = serializers.BooleanField()
    select_booster      = serializers.BooleanField()
    turbo_boost         = serializers.BooleanField()
    streaming           = serializers.BooleanField()

    price               = serializers.FloatField(min_value=0)
    choose_booster      = serializers.IntegerField()
    extend_order        = serializers.IntegerField()

    promo_code          = serializers.CharField()
    server              = serializers.CharField()

    # Order Info
    game_id = serializers.HiddenField(default=3)
    game_type = serializers.HiddenField(default='D')
    game_order_info = PubgDOI
    order_model = PubgDivisionOrder
    cryptomus = serializers.BooleanField(default=False, required=False, allow_null=True,)


    def validate(self, attrs):
        extend_order = attrs.get('extend_order', 0)
        pass_validate = False
        if extend_order > 0:
            pass_validate = self.extend_order_validate(attrs)
        if not pass_validate:
            self.booster_validate(attrs)
            self.validate_server(attrs.get('server'))
        return attrs

    def booster_validate(self, attrs):
        choose_booster = attrs.get('choose_booster', 0)
        select_booster = attrs.get('select_booster', False)
        if select_booster:
            try:
                Booster.objects.get(booster_id=choose_booster, is_pubg_player=True, can_choose_me=True)
            except Booster.DoesNotExist:
                raise serializers.ValidationError("Please select a valid booster")

    def extend_order_validate(self, attrs):
        extend_order = attrs.get('extend_order', 0)
        try:
            BaseOrder.objects.get(id=extend_order, game__id=3, game_type='D')
            return True
        except BaseOrder.DoesNotExist:
            raise serializers.ValidationError("This order can't be extended")
        

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if not data['select_booster']:
            data['choose_booster'] = 0
        return data

    def validate_server(self, value):
        extend_order = self.initial_data.get('extend_order', 0)
        if int(extend_order) <= 0:
            valid_servers = ["Europe", "Asia", "Middle East", "North America", "South America", "KRJP"]
            if value not in valid_servers:
                raise serializers.ValidationError("Invalid server selection")
        return value
