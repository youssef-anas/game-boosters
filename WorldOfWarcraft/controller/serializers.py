from rest_framework import serializers
from accounts.models import BaseOrder
from booster.models import Booster
from ..utils import get_rank_from_rp, extract_bundle_id
from WorldOfWarcraft.models import WorldOfWarcraftBundle

class ArenaSerializer(serializers.Serializer):
    current_rank = serializers.IntegerField(min_value=1, max_value=4, allow_null=True, required=False)
    current_RP = serializers.IntegerField(min_value=0, max_value=2500)
    desired_rank = serializers.IntegerField(min_value=1, max_value=4, allow_null=True, required=False)
    desired_RP = serializers.IntegerField(min_value=1, max_value=2500)
    is_arena_2vs2 = serializers.BooleanField()

    boost_method = serializers.ChoiceField(choices = (('self-play', 'self-play'), ('piloted', 'piloted'), ('remote-control', 'remote-control')))
    tournament_player = serializers.BooleanField()
    rank1_player = serializers.BooleanField()

    turbo_boost = serializers.BooleanField()
    streaming = serializers.BooleanField()

    server = serializers.CharField(max_length=300)
    price = serializers.FloatField(min_value=10)
    extend_order = serializers.IntegerField()
    promo_code = serializers.CharField()

    def validate(self, attrs):
        self.extend_order_validate(attrs)
        self.set_rank_values(attrs)
        return attrs 
    
    def set_rank_values(self, attrs):
        current_RP = attrs.get('current_RP', None)
        desired_RP = attrs.get('desired_RP', None)

        if current_RP >= desired_RP:
            raise serializers.ValidationError("Current RP must be less than desired RP")
        
        attrs['current_rank'] = get_rank_from_rp(current_RP)
        attrs['desired_rank'] = get_rank_from_rp(desired_RP)
        
            
    def extend_order_validate(self, attrs):
        extend_order = attrs.get('extend_order', '')
        if extend_order > 0:
            try:
                BaseOrder.objects.get(id=extend_order, game__id=6, game_type='D')
            except BaseOrder.DoesNotExist:
                raise serializers.ValidationError("This order can't be extended")            
    
    def validate_server(self, value):
        valid_servers = ["EU", "US"]
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

    turbo_boost = serializers.BooleanField()
    streaming = serializers.BooleanField()
    boost_method = serializers.ChoiceField(choices = (('self-play', 'self-play'), ('piloted', 'piloted'), ('remote-control', 'remote-control')))
    loot_priority = serializers.BooleanField()

    server = serializers.CharField(max_length=300)
    price = serializers.FloatField(min_value=10)
    promo_code = serializers.CharField()
    
    def validate_server(self, value):
        valid_servers = ["EU", "US"]
        if value not in valid_servers:
            raise serializers.ValidationError("Invalid server selection")
        return value


class RaidBundleSerializer(serializers.Serializer):
    bundle_id = serializers.CharField()

    turbo_boost = serializers.BooleanField()
    streaming = serializers.BooleanField()
    boost_method = serializers.ChoiceField(choices = (('self-play', 'self-play'), ('piloted', 'piloted'), ('remote-control', 'remote-control')))
    loot_priority = serializers.BooleanField()

    server = serializers.CharField(max_length=300)
    price = serializers.FloatField(min_value=10)
    promo_code = serializers.CharField()

    def validate_server(self, value):
        valid_servers = ["EU", "US"]
        if value not in valid_servers:
            raise serializers.ValidationError("Invalid server selection")
        return value
    
    def validate_bundle_id(self, value):
        try:
            bundle_id = extract_bundle_id(value)
            WorldOfWarcraftBundle.objects.get(id=bundle_id, mode=1)
            return bundle_id
        except WorldOfWarcraftBundle.DoesNotExist:
            raise serializers.ValidationError("Invalid Raid bundle")
            



class DungeonSimpleSerializer(serializers.Serializer):
    WOW_TRADER_CHOICES = [
        ("Personal Loot", "Personal Loot"),
        ("1 trader", "1 trader"),
        ("2 trader", "2 trader"),
        ("3 trader", "3 trader"),
        ("full-Priority", "full-Priority"),
    ]

    WOW_TRADER_ARMOR_CHOICES = [
        ("Cloth", "Cloth"),
        ("Leather", "Leather"),
        ("Mail", "Mail"),
        ("Plate", "Plate"),
    ]

    WOW_MAP_PREFERRED_CHOICES = [
        ("Random", "Random"),
        ("Specific", "Specific"),
    ]

    keystone = serializers.IntegerField(min_value=0, max_value=20)
    keys = serializers.IntegerField(min_value=0, max_value=20)

    # maps preferred 
    map_preferred = serializers.ChoiceField(choices = WOW_MAP_PREFERRED_CHOICES)

    algathar_academy = serializers.IntegerField(min_value=0, max_value=20)
    azure_vault = serializers.IntegerField(min_value=0, max_value=20)
    brackenhide_hollow = serializers.IntegerField(min_value=0, max_value=20)
    halls_of_infusion = serializers.IntegerField(min_value=0, max_value=20)
    neltharus = serializers.IntegerField(min_value=0, max_value=20)
    nokhud_offensive = serializers.IntegerField(min_value=0, max_value=20)
    ruby_life_pools = serializers.IntegerField(min_value=0, max_value=20)
    uldaman_legacy_of_tyr = serializers.IntegerField(min_value=0, max_value=20)

    # Traders
    traders = serializers.ChoiceField(choices = WOW_TRADER_CHOICES)
    traders_armor_type = serializers.ChoiceField(choices = WOW_TRADER_ARMOR_CHOICES, allow_blank=True)

    turbo_boost = serializers.BooleanField()
    streaming = serializers.BooleanField()
    timed = serializers.BooleanField()
    boost_method = serializers.ChoiceField(choices = (('self-play', 'self-play'), ('piloted', 'piloted'), ('remote-control', 'remote-control')))

    server = serializers.CharField(max_length=300)
    price = serializers.FloatField(min_value=10)
    promo_code = serializers.CharField()
    
    def validate_server(self, value):
        valid_servers = ["EU", "US"]
        if value not in valid_servers:
            raise serializers.ValidationError("Invalid server selection")
        return value
    
    # def validate(self, attrs):
        


class RaidLevelSerializer(serializers.Serializer):
    game_id = serializers.IntegerField(min_value=6, max_value=6)
    game_type = serializers.ChoiceField(choices = [('F', 'F')])

    current_level = serializers.IntegerField(min_value=1, max_value=80)
    desired_level = serializers.IntegerField(min_value=1, max_value=80)

    turbo_boost = serializers.BooleanField()
    streaming = serializers.BooleanField()

    server = serializers.ChoiceField(choices = [('EU', 'EU'), ('US', 'US')])
    price = serializers.FloatField(min_value=10)
    promo_code = serializers.CharField()
