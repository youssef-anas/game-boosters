from rest_framework import serializers


class RankedSerializer(serializers.Serializer):
  ranked_type = serializers.IntegerField(min_value=1, max_value=3)
  
  current_rank = serializers.IntegerField(min_value=1, max_value=7)
  current_division = serializers.IntegerField(min_value=1, max_value=3)
  desired_rank = serializers.IntegerField(min_value=1, max_value=8)
  desired_division = serializers.IntegerField(min_value=1, max_value=3)

  duo_boosting = serializers.BooleanField()
  select_booster = serializers.BooleanField()
  turbo_boost = serializers.BooleanField()
  streaming = serializers.BooleanField()

  price = serializers.FloatField(min_value=10)

  choose_booster = serializers.IntegerField()

  extend_order = serializers.IntegerField()

class PlacementSerializer(serializers.Serializer):
  last_rank = serializers.IntegerField(min_value=1, max_value=8)
  number_of_match = serializers.IntegerField(min_value=1, max_value=10)

  duo_boosting = serializers.BooleanField()
  select_booster = serializers.BooleanField()
  turbo_boost = serializers.BooleanField()
  streaming = serializers.BooleanField()

  price = serializers.FloatField(min_value=10)

  choose_booster = serializers.IntegerField()

  extend_order = serializers.IntegerField()

class SeasonalSerializer(serializers.Serializer):
  current_rank = serializers.IntegerField(min_value=1, max_value=8)
  number_of_wins = serializers.IntegerField(min_value=1, max_value=10)

  duo_boosting = serializers.BooleanField()
  select_booster = serializers.BooleanField()
  turbo_boost = serializers.BooleanField()
  streaming = serializers.BooleanField()

  price = serializers.FloatField(min_value=10)

  choose_booster = serializers.IntegerField()

  extend_order = serializers.IntegerField()

class TournamentSerializer(serializers.Serializer):
  current_league = serializers.IntegerField(min_value=1, max_value=8)

  duo_boosting = serializers.BooleanField()
  select_booster = serializers.BooleanField()
  turbo_boost = serializers.BooleanField()
  streaming = serializers.BooleanField()

  price = serializers.FloatField(min_value=10)

  choose_booster = serializers.IntegerField()

  extend_order = serializers.IntegerField()