from django.test import TestCase
from WorldOfWarcraft.models import WorldOfWarcraftRank

# Create your tests here.

class SetUp(TestCase):
    ranks = [
        WorldOfWarcraftRank(rank_name = 'Combatant', rank_image ='wow/images/0-1599.png'),
        WorldOfWarcraftRank(rank_name = 'Challenger', rank_image ='wow/images/1600-1799.png'),
        WorldOfWarcraftRank(rank_name = 'Rival', rank_image ='wow/images/1800-2099.png'),
        WorldOfWarcraftRank(rank_name = 'Duelist', rank_image ='wow/images/2100-2499.png'),
    ]
    ranks_queryset = WorldOfWarcraftRank.objects.bulk_create(ranks)