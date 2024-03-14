from rest_framework import serializers

class RankBoostSerializer(serializers.Serializer):

    current_rank = serializers.IntegerField(min_value=1, max_value=8)
    desired_rank = serializers.IntegerField(min_value=1, max_value=8)

    # division
    current_division = serializers.IntegerField(min_value=0, max_value=8000)
    desired_division = serializers.IntegerField(min_value=500, max_value=8000)

    # Role
    role = serializers.IntegerField(min_value=1, max_value=2)

    # exra filds about order
    duo_boosting = serializers.BooleanField()
    select_booster = serializers.BooleanField()
    turbo_boost = serializers.BooleanField()
    streaming = serializers.BooleanField()
    # select_champion = serializers.BooleanField()

    server = serializers.CharField(max_length=300)

    price = serializers.FloatField(min_value=10)

    choose_booster = serializers.IntegerField()

    extend_order = serializers.IntegerField()

    promo_code = serializers.CharField()


class PlacementSerializer(serializers.Serializer):
    last_rank = serializers.IntegerField(min_value=1, max_value=8)
    last_division = serializers.IntegerField(min_value=0, max_value=8000)
    number_of_match = serializers.IntegerField(min_value=1, max_value=10)

    # Role
    role = serializers.IntegerField(min_value=1, max_value=2)

    duo_boosting = serializers.BooleanField()
    select_booster = serializers.BooleanField()
    turbo_boost = serializers.BooleanField()
    streaming = serializers.BooleanField()
    # select_champion = serializers.BooleanField()

    server = serializers.CharField(max_length=300)

    price = serializers.FloatField(min_value=10)

    choose_booster = serializers.IntegerField()

    extend_order = serializers.IntegerField()

    promo_code = serializers.CharField()