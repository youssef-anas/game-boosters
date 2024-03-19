from django.test import TestCase
from dota2.models import Dota2Rank, Dota2Placement, Dota2MmrPrice
import json
import math

# Create your tests here.
class SetUp(TestCase):
  ranks = [
    Dota2Rank(rank_name = 'herald', rank_image = 'dota2/images/herald.png', start_RP = 0, end_RP = 700),

    Dota2Rank(rank_name = 'guardian', rank_image = 'dota2/images/guardian.png', start_RP = 701, end_RP = 1540),

    Dota2Rank(rank_name = 'crusader', rank_image = 'dota2/images/crusader.png', start_RP = 1541, end_RP = 2380),

    Dota2Rank(rank_name = 'archon', rank_image = 'dota2/images/archon.png', start_RP = 2381, end_RP = 3220),

    Dota2Rank(rank_name = 'legend', rank_image = 'dota2/images/legend.png', start_RP = 3221, end_RP = 4060),

    Dota2Rank(rank_name = 'ancient', rank_image = 'dota2/images/ancient.png', start_RP = 4061, end_RP = 4900),

    Dota2Rank(rank_name = 'divine', rank_image = 'dota2/images/divine.png', start_RP = 4901, end_RP = 5500),

    Dota2Rank(rank_name = 'immortal', rank_image = 'dota2/images/immortal.webp', start_RP = 5501, end_RP = 8000),
  ]

  price = [
    Dota2MmrPrice(price_0_2000 = 3.98, price_2000_3000 = 4.63, price_3000_4000 = 5.82, price_4000_5000 = 10.65, price_5000_5500 = 19.86, price_5500_6000 = 24.46, price_6000_extra = 38.01)
  ]

  placements = [
    Dota2Placement(rank_name = 'herald', rank_image = 'dota2/images/herald.png', start_RP = 0, end_RP = 700, price = 1.91),

    Dota2Placement(rank_name = 'guardian', rank_image = 'dota2/images/guardian.png', start_RP = 701, end_RP = 1540, price = 1.92),

    Dota2Placement(rank_name = 'crusader', rank_image = 'dota2/images/crusader.png', start_RP = 1541, end_RP = 2380, price = 1.93),

    Dota2Placement(rank_name = 'archon', rank_image = 'dota2/images/archon.png', start_RP = 2381, end_RP = 3220, price = 1.94),

    Dota2Placement(rank_name = 'legend', rank_image = 'dota2/images/legend.png', start_RP = 3221, end_RP = 4060, price = 1.95),

    Dota2Placement(rank_name = 'ancient', rank_image = 'dota2/images/ancient.png', start_RP = 4061, end_RP = 4900, price = 1.96),

    Dota2Placement(rank_name = 'divine', rank_image = 'dota2/images/divine.png', start_RP = 4901, end_RP = 5500, price = 1.97),

    Dota2Placement(rank_name = 'immortal', rank_image = 'dota2/images/immortal.webp', start_RP = 5501, end_RP = 8000, price = 1.98),
  ]

  ranks_queryset = Dota2Rank.objects.bulk_create(ranks)
  price_queryset = Dota2MmrPrice.objects.bulk_create(price)
  placements_queryset = Dota2Placement.objects.bulk_create(placements)