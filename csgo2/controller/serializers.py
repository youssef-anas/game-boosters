from rest_framework import serializers

class DivisionSerializer(serializers.Serializer):
    current_rank = serializers.IntegerField(min_value=1, max_value=17)
    desired_rank = serializers.IntegerField(min_value=1, max_value=18)
    
    duo_boosting = serializers.BooleanField()
    select_booster = serializers.BooleanField()
    turbo_boost = serializers.BooleanField()
    streaming = serializers.BooleanField()

    server = serializers.CharField(max_length=300)

    price = serializers.FloatField(min_value=10)

    choose_booster = serializers.IntegerField()

    extend_order = serializers.IntegerField()

    promo_code = serializers.CharField()


class PremierSerializer(serializers.Serializer):
    current_rank = serializers.IntegerField(min_value=1, max_value=8)
    desired_rank = serializers.IntegerField(min_value=1, max_value=8)

    # division
    current_division = serializers.IntegerField(min_value=0, max_value=30000)
    desired_division = serializers.IntegerField(min_value=500, max_value=30000)


    # exra filds about order
    duo_boosting = serializers.BooleanField()
    select_booster = serializers.BooleanField()
    turbo_boost = serializers.BooleanField()
    streaming = serializers.BooleanField()

    server = serializers.CharField(max_length=300)

    price = serializers.FloatField(min_value=10)

    choose_booster = serializers.IntegerField()

    extend_order = serializers.IntegerField()

    promo_code = serializers.CharField()

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

    extend_order = serializers.IntegerField()

    promo_code = serializers.CharField()