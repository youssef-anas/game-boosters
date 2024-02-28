from rest_framework import serializers

class RankBoostSerializer(serializers.Serializer):

    # rank
    current_rank = serializers.IntegerField(min_value=1, max_value=4)
    desired_rank = serializers.IntegerField(min_value=1, max_value=4)

    # division
    current_division = serializers.IntegerField(min_value=0, max_value=2500)
    current_division = serializers.IntegerField(min_value=1, max_value=2500)

    # mark ??
    # add here TODO
    

    # exra filds about order
    duo_boosting = serializers.BooleanField()
    select_booster = serializers.BooleanField()
    turbo_boost = serializers.BooleanField()
    streaming = serializers.BooleanField()
    choose_booster = serializers.IntegerField()
    extend_order = serializers.IntegerField()



    # fild not fo all games
    choose_agents = serializers.BooleanField()

    # for this game only
    role = serializers.IntegerField(min_value=1, max_value=2)
    
