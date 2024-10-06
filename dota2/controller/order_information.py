from django.shortcuts import get_object_or_404
import json
from django.utils import timezone
from dota2.models import Dota2MmrPrice, BaseOrder
from accounts.models import PromoCode
from booster.models import Booster
import math
from dota2.utils import get_division_prices, get_placement_prices

# Ranking System
# Herald — 0-769 MMR.
# Guardian — 770-1539 MMR.
# Crusader — 1540-2309 MMR.
# Archon — 2310-3079 MMR.
# Legend — 3080-3849 MMR.
# Ancient — 3850-4619 MMR.
# Divine — 4620-5420 MMR.
# Immortal — ∽6000+ MMR.

rank_names = ['UNRANK', 'HERALD', 'GUARDIAN', 'CRUSADER', 'ARCHON', 'LEGEND', 'ANCIENT', 'DIVINE', 'IMMORTAL']
role_names = ['NoRole', 'Core', 'Support']
ROLE_PRICES = [0, 0, 0.30]
def get_rank_boost_order_result_by_rank(data):
  MIN_DESIRED_VALUE = 50
  # Division
  # with open('static/dota2/data/prices.json', 'r') as file:
  #   prices = json.load(file)
  #   pass

  divison_prices = get_division_prices()
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
  # Ranks
  current_rank = data['current_rank']
  desired_rank = data['desired_rank']

  # Division
  current_division = data['current_division']
  desired_division = data['desired_division']

  # Role
  role = data['role']

  total_percent = 0

  duo_boosting = data['duo_boosting']
  select_booster = data['select_booster']
  turbo_boost = data['turbo_boost']
  streaming = data['streaming']
  # select_champion = data['select_champion']
  
  extend_order_id = data['extend_order']
  server = data['server']
  promo_code = data['promo_code']
  promo_code_id = 0

  duo_boosting_value = 0
  select_booster_value = 0
  turbo_boost_value = 0
  streaming_value = 0
  
  select_champion_value = 0

  promo_code_amount = 0

  boost_options = []

  if duo_boosting:
    total_percent += 0.65
    boost_options.append('DUO BOOSTING')
    duo_boosting_value = 1

  if select_booster:
    total_percent += 0.10
    boost_options.append('SELECT BOOSTING')
    select_booster_value = 1

  if turbo_boost:
    total_percent += 0.20
    boost_options.append('TURBO BOOSTING')
    turbo_boost_value = 1
  
  if streaming:
    total_percent += 0.15
    boost_options.append('STREAMING')
    streaming_value = 1

  # if select_champion:
  #   total_percent += 0.0
  #   boost_options.append('CHOOSE AGENTS')
  #   select_champion_value = 1

  if promo_code != 'null':   
    try:
      promo_code_obj = PromoCode.objects.get(code=promo_code)
      promo_code_amount = promo_code_obj.discount_amount
      promo_code_id = promo_code_obj.pk
    except PromoCode.DoesNotExist:
      promo_code_amount = 0
  
  curent_mmr_in_c_range, current_range = get_range_current(current_division)
  desired_mmr_in_d_range, derired_range = get_range_desired(desired_division)
  sliced_prices = full_price_val[current_range : derired_range - 1]
  sum_current = curent_mmr_in_c_range * divison_prices[current_range]
  sum_desired = desired_mmr_in_d_range * divison_prices[derired_range]
  clear_res = sum(sliced_prices)
  # full price for all rank [159.2, 92.6, 116.4, 213, 198.6, 244.6, 1520.4]

  if current_range == derired_range:
    range_value = math.floor((desired_division - current_division ) / MIN_DESIRED_VALUE)
    price = round(range_value * divison_prices[current_range], 2)
  else:
    price = round(sum_current + sum_desired + clear_res,2)

  total_Percentage_with_role_result = total_percent + ROLE_PRICES[role]
  
  price += price * total_Percentage_with_role_result

  price -= price * (promo_code_amount / 100)

  price = round(price, 2)

  if extend_order_id > 0:
    try:
      extend_order = BaseOrder.objects.get(id=extend_order_id)
      extend_order_price = extend_order.price
      price = round(price - extend_order_price, 2)
    except:
      pass

  booster_id = data['choose_booster']
  if booster_id > 0 :
    get_object_or_404(Booster, booster_id=booster_id, booster__is_booster=True, is_dota2_player=True)
  else:
    booster_id = 0
  
  invoice = f'DOTA2-10-A-{current_rank}-{current_division}-0-{desired_rank}-{desired_division}-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{extend_order_id}-{server}-{price}-{select_champion_value}-{promo_code_id}-{role}-0-0-0-{timezone.now()}'
  
  invoice_with_timestamp = str(invoice)

  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'DOTA2, BOOSTING FROM {rank_names[current_rank]} {current_division} TO {rank_names[desired_rank]} {desired_division}{boost_string} ROLE: {role_names[role]}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})

def get_palcement_order_result_by_rank(data):
  # Placement
  placement_price = get_placement_prices()
  
  last_rank = data['last_rank']
  last_division = data['last_division']
  number_of_match = data['number_of_match']

  # Role
  role = data['role']

  total_percent = 0
  
  duo_boosting = data['duo_boosting']
  select_booster = data['select_booster']
  turbo_boost = data['turbo_boost']
  streaming = data['streaming']
  # select_champion = data['select_champion']

  extend_order_id = data['extend_order']
  server = data['server']
  promo_code = data['promo_code']

  promo_code_id = 0

  duo_boosting_value = 0
  select_booster_value = 0
  turbo_boost_value = 0
  streaming_value = 0
  select_champion_value = 0

  promo_code_amount = 0

  boost_options = []

  if duo_boosting:
    total_percent += 0.65
    boost_options.append('DUO BOOSTING')
    duo_boosting_value = 1

  if select_booster:
    total_percent += 0.10
    boost_options.append('SELECT BOOSTING')
    select_booster_value = 1

  if turbo_boost:
    total_percent += 0.20
    boost_options.append('TURBO BOOSTING')
    turbo_boost_value = 1
  
  if streaming:
    total_percent += 0.15
    boost_options.append('STREAMING')
    streaming_value = 1

  # if select_champion:
  #   total_percent += 0.0
  #   boost_options.append('CHOOSE AGENTS')
  #   select_champion_value = 1

  if promo_code != 'null':   
    try:
      promo_code_obj = PromoCode.objects.get(code=promo_code)
      promo_code_amount = promo_code_obj.discount_amount
      promo_code_id = promo_code_obj.pk
    except PromoCode.DoesNotExist:
      promo_code_amount = 0

  price = placement_price[last_rank - 1] * number_of_match

  total_Percentage_with_role_result = total_percent + ROLE_PRICES[role]

  price += (price * total_Percentage_with_role_result)

  price -= price * (promo_code_amount/100)

  price = round(price, 2)

  if extend_order_id > 0:
    try:
      extend_order = BaseOrder.objects.get(id=extend_order_id)
      extend_order_price = extend_order.price
      price = round(price - extend_order_price, 2)
    except:
      pass

  booster_id = data['choose_booster']
  if booster_id > 0 :
    get_object_or_404(Booster, booster_id=booster_id, booster__is_booster=True, is_dota2_player=True)
  else:
    booster_id = 0

  invoice = f'DOTA2-10-P-{last_rank}-{number_of_match}-{last_division}-none-none-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{extend_order_id}-{server}-{price}-{select_champion_value}-{promo_code_id}-{role}-0-0-0-{timezone.now()}'

  invoice_with_timestamp = str(invoice)

  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'DOTA2, BOOSTING OF {number_of_match} Start With {rank_names[last_rank]}{boost_string}  ROLE: {role_names[role]}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})

from gameBoosterss.order_info.orders import BaseOrderInfo,ExtendOrder
from gameBoosterss.order_info.arena_v2 import Arena_V2_GameOrderInfo
from gameBoosterss.order_info.placement import PlacementGameOrderInfo

class Dota2_AOI(BaseOrderInfo, ExtendOrder, Arena_V2_GameOrderInfo):
  arena_prices = get_division_prices()
  price1 = round(arena_prices[0]*40,1)
  price2 = round(arena_prices[1]*20,1)
  price3 = round(arena_prices[2]*20,1)
  price4 = round(arena_prices[3]*20,1)
  price5 = round(arena_prices[4]*10,1)
  price6 = round(arena_prices[5]*10,1)
  price7 = round(arena_prices[6]*40,1) 
  full_price_val = [price1, price2, price3, price4, price5, price6, price7]
  points_range = [2000, 3000, 4000, 5000, 5500, 6000, 8000]
  points_value = 50
  floor = True

  def get_game_info(self):
    super().get_game_info()
    self.game_order.update({'role': self.data['role']})


  def get_game_info_extended(self):
    super().get_game_info_extended()
    self.game_order.update({'role': self.extend_game.role})

  def get_totla_percent_price(self):
    super().get_totla_percent_price()
    if self.data['role'] == 2:
      self.total_percent += 30

class Dota2_POI(BaseOrderInfo, ExtendOrder, PlacementGameOrderInfo): 
  placement_data = get_placement_prices()
  
  def get_game_info(self):
    super().get_game_info()
    self.game_order.update({'role': self.data['role']})

  def get_totla_percent_price(self):
    super().get_totla_percent_price()
    if self.data['role'] == 2:
      self.total_percent += 30

  
