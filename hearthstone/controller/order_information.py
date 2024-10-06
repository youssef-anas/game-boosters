from django.shortcuts import get_object_or_404
from wildRift.models import *
from django.shortcuts import get_object_or_404
from django.utils import timezone
from accounts.models import PromoCode
from booster.models import Booster
from hearthstone.utils import get_hearthstone_divisions_data, get_hearthstone_marks_data, get_hearthstone_battle_prices
import math


division_names = ['','X','IX','VIII','VII','VI','V','IV','III','II','I']
rank_names = ['UNRANK', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND', 'LEGEND']

def get_division_order_result_by_rank(data):
  # Division
  current_rank = data['current_rank']
  current_division = data['current_division']
  marks = data['marks']
  desired_rank = data['desired_rank']
  desired_division = data['desired_division']

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
  # select_champion_value = 0
  streaming_value = 0
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
    boost_options.append('TURBO BOOST')
    turbo_boost_value = 1
  
  if streaming:
    total_percent += 0.15
    boost_options.append('STREAMING')
    streaming_value = 1

  # if select_champion:
  #   total_percent += 0.0
  #   boost_options.append('CHOOSE LEGENDS')
  #   select_champion_value = 1
    
  if promo_code != 'null':   
    try:
      promo_code_obj = PromoCode.objects.get(code=promo_code)
      promo_code_amount = promo_code_obj.discount_amount
      promo_code_id = promo_code_obj.pk
    except PromoCode.DoesNotExist:
      promo_code_amount = 0

  # Read data from utils file
  division_price = get_hearthstone_divisions_data()
  flattened_data = [item for sublist in division_price for item in sublist]
  flattened_data.insert(0,0)
  ##
  
  marks_data = get_hearthstone_marks_data()
  marks_data.insert(0,[0,0,0])
  ##    
  start_division = ((current_rank-1) * 10) + current_division
  end_division = ((desired_rank-1) * 10)+ desired_division
  marks_price = marks_data[current_rank][marks]
  sublist = flattened_data[start_division:end_division ]
  total_sum = sum(sublist)
  price = total_sum - marks_price
  price += (price * total_percent)
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
    get_object_or_404(Booster, booster_id=booster_id, booster__is_booster=True, is_hearthstone_player=True)
  else:
    booster_id = 0

  invoice = f'HS-7-D-{current_rank}-{current_division}-{marks}-{desired_rank}-{desired_division}-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{extend_order_id}-{server}-{price}-0-{promo_code_id}-0-0-0-0-{timezone.now()}'

  invoice_with_timestamp = str(invoice)
  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'HEARTHSTONE, BOOSTING FROM {rank_names[current_rank]} {division_names[current_division]} MARKS {marks} TO {rank_names[desired_rank]} {division_names[desired_division]}{boost_string}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})



def get_battle_order_result(data):

  def get_range_current(amount):
    MAX_LISTS = [1999, 3999, 5999, 7999, 10000]
    for idx, max_val in enumerate(MAX_LISTS, start=1):
        if amount <= max_val:
            val = max_val - amount
            return round(val / 25, 2), idx
    print('out_of_range')
    return None, None
    
  def get_range_desired(amount):
      MAX_LISTS = [1999, 3999, 5999, 7999, 10000]
      for idx, max_val in enumerate(MAX_LISTS, start=1):
          if amount <= max_val:
              val = amount-MAX_LISTS[idx-2]
              return round(val / 25, 2), idx
      print('out_of_range')
      return None, None


  # Division
  current_rank = 1
  current_division = data['current_mmr']
  marks = 0
  desired_rank = 1
  desired_division = data['desired_mmr']

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
  # select_champion_value = 0
  streaming_value = 0
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
    boost_options.append('TURBO BOOST')
    turbo_boost_value = 1
  
  if streaming:
    total_percent += 0.15
    boost_options.append('STREAMING')
    streaming_value = 1

  # if select_champion:
  #   total_percent += 0.0
  #   boost_options.append('CHOOSE LEGENDS')
  #   select_champion_value = 1
    
  if promo_code != 'null':   
    try:
      promo_code_obj = PromoCode.objects.get(code=promo_code)
      promo_code_amount = promo_code_obj.discount_amount
      promo_code_id = promo_code_obj.pk
    except PromoCode.DoesNotExist:
      promo_code_amount = 0

  # Read data from utils file
  battle_price = get_hearthstone_battle_prices()

  price1 = round(battle_price[0] * 80 , 2)
  price2 = round(battle_price[1] * 80 , 2)
  price3 = round(battle_price[2] * 80 , 2)
  price4 = round(battle_price[3] * 80 , 2)
  price5 = round(battle_price[4] * 80 , 2)
  full_price_val = [price1, price2, price3, price4, price5]

  ##
  curent_mmr_in_c_range, current_range = get_range_current(current_division)
  desired_mmr_in_d_range, derired_range = get_range_desired(desired_division)
  sliced_prices = full_price_val[current_range : derired_range-1]
  sum_current = curent_mmr_in_c_range * battle_price[current_range-1]
  sum_desired = desired_mmr_in_d_range * battle_price[derired_range-1]
  clear_res = sum(sliced_prices)

  if current_range == derired_range:
      range_value = math.floor((desired_division - current_division ) / 25)
      price = round(range_value * battle_price[current_range-1], 2)
  else:
      price = round(sum_current + sum_desired + clear_res,2)



  price += (price * total_percent)
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
    get_object_or_404(Booster, booster_id=booster_id, booster__is_booster=True, is_hearthstone_player=True)
  else:
    booster_id = 0

  invoice = f'HS-7-A-{current_rank}-{current_division}-{marks}-{desired_rank}-{desired_division}-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{extend_order_id}-{server}-{price}-0-{promo_code_id}-0-0-0-0-{timezone.now()}'

  invoice_with_timestamp = str(invoice)
  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'HEARTHSTONE, BOOSTING FROM  {current_division} MMR TO {desired_division} MMR {boost_string}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})

from gameBoosterss.order_info.orders import BaseOrderInfo,ExtendOrder
from gameBoosterss.order_info.division import DivisionGameOrderInfo
from gameBoosterss.order_info.arena_v2 import Arena_V2_GameOrderInfo

class HS_DOI(BaseOrderInfo, ExtendOrder, DivisionGameOrderInfo):
    division_prices_data = get_hearthstone_divisions_data()
    division_prices = [item for sublist in division_prices_data for item in sublist]
    division_prices.insert(0, 0)
    marks_data = get_hearthstone_marks_data()
    marks_data.insert(0, [0, 0, 0, 0, 0, 0])
    division_number = 10

class HS_AOI(BaseOrderInfo, ExtendOrder, Arena_V2_GameOrderInfo):
    arena_prices = get_hearthstone_battle_prices()
    price1 = round(arena_prices[0] * 80 , 2)
    price2 = round(arena_prices[1] * 80 , 2)
    price3 = round(arena_prices[2] * 80 , 2)
    price4 = round(arena_prices[3] * 80 , 2)
    price5 = round(arena_prices[4] * 80 , 2)
    full_price_val = [price1, price2, price3, price4, price5]
    points_range = [1999, 3999, 5999, 7999, 10000]
    points_value = 25