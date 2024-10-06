from django.shortcuts import get_object_or_404
from wildRift.models import *
import json
from django.shortcuts import get_object_or_404
from django.utils import timezone
from accounts.models import PromoCode
from booster.models import Booster
from mobileLegends.utils import get_mobile_legends_placements_data, get_mobile_legends_marks_data, get_mobile_legends_divisions_data

division_names = ['','IV','III','II','I']  
rank_names = ['Unranked','warrior', 'elite', 'master', 'grandmaster', 'epic', 'legend', 'mythic', 'mythical honor', 'mythical glory', 'mythical immortal']

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
  select_champion = False
  promo_code_amount = 0

  extend_order_id = data['extend_order']
  server = data['server']
  promo_code = data['promo_code']
  promo_code_id = 0

  duo_boosting_value = 0
  select_booster_value = 0
  turbo_boost_value = 0
  streaming_value = 0
  select_champion_value = 0

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

  if select_champion:
    total_percent += 0.0
    boost_options.append('CHOOSE CHAMPIONS')
    select_champion_value = 1

  if promo_code != 'null': 
    try:
      promo_code_obj = PromoCode.objects.get(code=promo_code)
      promo_code_amount = promo_code_obj.discount_amount
      promo_code_id = promo_code_obj.pk
    except PromoCode.DoesNotExist:
      promo_code_amount = 0

  # Read data using utility functions
  division_price = get_mobile_legends_divisions_data()
  flattened_data = [item for sublist in division_price for item in sublist]
  flattened_data.insert(0, 0)

  marks_data = get_mobile_legends_marks_data()
  # marks_data.insert(0, [0, 0, 0, 0, 0, 0])
    
  # if current_rank == 1:
  #   if current_division not in [3, 4, 5]:
  #     print(f"error in current division cant be {current_division} in rank {current_rank}")
  #     current_division = 3
  #   if marks not in [1,2,3]:
  #     print(f"error in current mark cant be {marks} in rank {current_rank}")
  #     marks = 3

  # elif current_rank == 2 :
  #   if current_division not in [2, 3, 4, 5]:
  #     print(f"error in current rank cant be {current_division} in rank {current_rank}")
  #     current_division = 2
  #   if marks not in [1,2,3]:
  #     print(f"error in current mark cant be {marks} in rank {current_rank}")
  #     marks = 3

  # elif current_rank == 3 :
  #   if current_division not in [2, 3, 4, 5]:
  #     print(f"error in current rank cant be {current_division} in rank {current_rank}")
  #     current_division = 2
  #   if marks not in [1,2,3,4]:
  #     print(f"error in current mark cant be {marks} in rank {current_rank}")
  #     marks = 4 

  # elif current_rank in [4, 5, 6] :
  #   if current_division not in [1, 2, 3, 4, 5]:
  #     print(f"error in current rank cant be {current_division} in rank {current_rank}")
  #     current_division = 1
  #   if marks not in [1,2,3,4,5]:
  #     print(f"error in current mark cant be {marks} in rank {current_rank}")
  #     marks = 1

  # elif current_rank in [7, 8, 9] :
  #   if current_division not in [1, 2, 3, 4, 5]:
  #     print(f"error in current rank cant be {current_division} in rank {current_rank}")
  #     current_division = 1
  #   if marks not in [1,2,3,4,5]:
  #     print(f"error in current mark cant be {marks} in rank {current_rank}")
  #     marks = 0
  # else:
  #   raise IndexError 

  if desired_rank > 10 or desired_rank < 0:
    raise IndexError 


  #########################  
  start_division = ((current_rank-1) * 5) + current_division
  end_division = ((desired_rank-1) * 5)+ desired_division
  marks_price = marks_data[current_rank][marks]
  
  sublist = flattened_data[start_division:end_division ]
  total_sum = sum(sublist)
  print(sublist)
  print("marks_data", marks_data)
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
    get_object_or_404(Booster, booster_id=booster_id, booster__is_booster=True, is_mobleg_player=True)
  else:
    booster_id = 0
  invoice = f'MOBLEG-8-D-{current_rank}-{current_division}-{marks}-{desired_rank}-{desired_division}-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{extend_order_id}-{server}-{price}-{select_champion_value}-{promo_code_id}-0-0-0-{timezone.now()}'

  invoice_with_timestamp = str(invoice)
  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'MOBLEG, BOOSTING FROM {rank_names[current_rank]} {division_names[current_division]} STARS {marks} TO {rank_names[desired_rank]} {division_names[desired_division]}{boost_string}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})

def get_placement_order_result_by_rank(data):
  last_rank = data['last_rank']
  number_of_match = data['number_of_match']

  total_percent = 0

  duo_boosting = data['duo_boosting']
  select_booster = data['select_booster']
  turbo_boost = data['turbo_boost']
  streaming = data['streaming']
  select_champion = False

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

  if select_champion:
    total_percent += 0.0
    boost_options.append('CHOOSE CHAMPIONS')
    select_champion_value = 1

  if promo_code != 'null': 
    try:
      promo_code_obj = PromoCode.objects.get(code=promo_code)
      promo_code_amount = promo_code_obj.discount_amount
      promo_code_id = promo_code_obj.pk
    except PromoCode.DoesNotExist:
      promo_code_amount = 0

  # Read data using utility functions
  placement_data = get_mobile_legends_placements_data()
  
  price = placement_data[last_rank] * number_of_match
  price += (price * total_percent)
  price -= price * (promo_code_amount/100)
  price = round(price, 2)


  booster_id = data['choose_booster']
  if booster_id > 0 :
    get_object_or_404(Booster, booster_id=booster_id, booster__is_booster=True, is_mobleg_player=True)
  else:
    booster_id = 0

  invoice = f'MOBLEG-8-P-{last_rank}-{number_of_match}-0-0-0-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{0}-{server}-{price}-{select_champion_value}-{promo_code_id}-0-0-0-0-{timezone.now()}'

  invoice_with_timestamp = str(invoice)
  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'MOBLEG, BOOSTING OF {number_of_match} Start With {rank_names[last_rank]}{boost_string}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})

from gameBoosterss.order_info.orders import BaseOrderInfo,ExtendOrder
from gameBoosterss.order_info.division import DivisionGameOrderInfo
from gameBoosterss.order_info.placement import PlacementGameOrderInfo

class MOBLEG_DOI(BaseOrderInfo, ExtendOrder, DivisionGameOrderInfo):
    division_prices_data = get_mobile_legends_divisions_data()
    division_prices = [item for sublist in division_prices_data for item in sublist]
    division_prices.insert(0, 0)
    marks_data = get_mobile_legends_marks_data()
    marks_data.insert(0, [0, 0, 0, 0, 0, 0, 0, 0])
    division_number = 5

class MOBLEG_POI(BaseOrderInfo, PlacementGameOrderInfo):
  placement_data = get_mobile_legends_placements_data()