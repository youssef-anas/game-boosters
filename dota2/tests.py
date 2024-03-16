from django.test import TestCase
from dota2.models import Dota2Rank, Dota2Placement, Dota2MmrPrice
import json
import math

# Create your tests here.
class SetUp(TestCase):
    with open('static/dota2/data/prices.json', 'r') as file:
      prices = json.load(file)
      pass

    divison_prices = prices['division']
    divison_prices.insert(0,0)
    price1 = round(divison_prices[1]*40,1)
    price2 = round(divison_prices[2]*20,1)
    price3 = round(divison_prices[3]*20,1)
    price4 = round(divison_prices[4]*20,1)
    price5 = round(divison_prices[5]*10,1)
    price6 = round(divison_prices[6]*10,1)
    price7 = round(divison_prices[7]*40,1) 
    full_price_val = [price1, price2, price3, price4, price5, price6, price7]

    def get_range_current(mmr):
        MAX_LISTS = [2000, 3000, 4000, 5000, 5500, 6000, 8000]
        for idx, max_val in enumerate(MAX_LISTS, start=1):
            if mmr <= max_val:
                val = max_val - mmr
                return math.floor(val/50), idx
        print('out_of_range')
        return None, None
        
    def get_range_desired(mmr):
        MAX_LISTS = [2000, 3000, 4000, 5000, 5500, 6000, 8000]
        for idx, max_val in enumerate(MAX_LISTS, start=1):
            if mmr <= max_val:
                val = mmr-MAX_LISTS[idx-2]
                return math.floor(val/50), idx
        print('out_of_range')
        return None, None
    
    curent_mmr_in_c_range, current_range = get_range_current(2300)        
    desired_mmr_in_d_range, derired_range = get_range_desired(6700)
    sliced_prices = full_price_val[current_range :derired_range - 1]
    sum_current = curent_mmr_in_c_range * divison_prices[current_range]
    sum_desired = desired_mmr_in_d_range * divison_prices[derired_range]
    clear_res = sum(sliced_prices)
   # full price for all rank [159.2, 92.6, 116.4, 213, 198.6, 244.6, 1520.4]
    result = round(sum_current + sum_desired + clear_res,2)


























  # ranks = [
  #   Dota2Rank(rank_name = 'herald', rank_image = 'dota2/images/herald.png', start_RP = 0, end_RP = 700),

  #   Dota2Rank(rank_name = 'guardian', rank_image = 'dota2/images/guardian.png', start_RP = 701, end_RP = 1540),

  #   Dota2Rank(rank_name = 'crusader', rank_image = 'dota2/images/crusader.png', start_RP = 1541, end_RP = 2380),

  #   Dota2Rank(rank_name = 'archon', rank_image = 'dota2/images/archon.png', start_RP = 2381, end_RP = 3220),

  #   Dota2Rank(rank_name = 'legend', rank_image = 'dota2/images/legend.png', start_RP = 3221, end_RP = 4060),

  #   Dota2Rank(rank_name = 'ancient', rank_image = 'dota2/images/ancient.png', start_RP = 4061, end_RP = 4900),

  #   Dota2Rank(rank_name = 'divine', rank_image = 'dota2/images/divine.png', start_RP = 4901, end_RP = 5500),

  #   Dota2Rank(rank_name = 'immortal', rank_image = 'dota2/images/immortal.webp', start_RP = 5501, end_RP = 8000),
  # ]

  # price = [
  #   Dota2MmrPrice(price_0_2000 = 3.98, price_2000_3000 = 4.63, price_3000_4000 = 5.82, price_4000_5000 = 10.65, price_5000_5500 = 19.86, price_5500_6000 = 24.46, price_6000_extra = 38.01)
  # ]

  # placements = [
  #   Dota2Placement(rank_name = 'herald', rank_image = 'dota2/images/herald.png', start_RP = 0, end_RP = 700, price = 1.91),

  #   Dota2Placement(rank_name = 'guardian', rank_image = 'dota2/images/guardian.png', start_RP = 701, end_RP = 1540, price = 1.92),

  #   Dota2Placement(rank_name = 'crusader', rank_image = 'dota2/images/crusader.png', start_RP = 1541, end_RP = 2380, price = 1.93),

  #   Dota2Placement(rank_name = 'archon', rank_image = 'dota2/images/archon.png', start_RP = 2381, end_RP = 3220, price = 1.94),

  #   Dota2Placement(rank_name = 'legend', rank_image = 'dota2/images/legend.png', start_RP = 3221, end_RP = 4060, price = 1.95),

  #   Dota2Placement(rank_name = 'ancient', rank_image = 'dota2/images/ancient.png', start_RP = 4061, end_RP = 4900, price = 1.96),

  #   Dota2Placement(rank_name = 'divine', rank_image = 'dota2/images/divine.png', start_RP = 4901, end_RP = 5500, price = 1.97),

  #   Dota2Placement(rank_name = 'immortal', rank_image = 'dota2/images/immortal.webp', start_RP = 5501, end_RP = 8000, price = 1.98),
  # ]

  # ranks_queryset = Dota2Rank.objects.bulk_create(ranks)
  # price_queryset = Dota2MmrPrice.objects.bulk_create(price)
  # placements_queryset = Dota2Placement.objects.bulk_create(placements)