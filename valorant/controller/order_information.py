from django.shortcuts import get_object_or_404
from django.utils import timezone
from accounts.models import PromoCode, BaseOrder
from booster.models import Booster
from valorant.utils import get_valorant_divisions_data, get_valorant_marks_data, get_valorant_placements_data

division_names = ['','I','II','III']  
rank_names = ['UNRANK', 'IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND', 'ASCENDANT', 'IMMORTAL']

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
  select_champion = data['select_champion']
  champions_data = data['champion_data']

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

  if select_champion:
    total_percent += 0.0
    boost_options.append('CHOOSE AGENTS')
    select_champion_value = 1

  if promo_code != 'null':   
    try:
      promo_code_obj = PromoCode.objects.get(code=promo_code)
      promo_code_amount = promo_code_obj.discount_amount
      promo_code_id = promo_code_obj.pk
    except PromoCode.DoesNotExist:
      promo_code_amount = 0

  # Read data from utility functions
  divisions_data = get_valorant_divisions_data()
  flattened_data = [item for sublist in divisions_data for item in sublist]
  flattened_data.insert(0, 0)

  marks_data = get_valorant_marks_data()
  marks_data.insert(0, [0, 0, 0, 0, 0, 0])

  start_division = ((current_rank-1) * 3) + current_division
  end_division = ((desired_rank-1) * 3)+ desired_division
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
    get_object_or_404(Booster, booster_id=booster_id, booster__is_booster=True, is_valo_player=True)
  else:
    booster_id = 0

  invoice = f'valo-2-D-{current_rank}-{current_division}-{marks}-{desired_rank}-{desired_division}-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{extend_order_id}-{server}-{price}-{select_champion_value}-{promo_code_id}-0-0-0-{champions_data}-{timezone.now()}'

  invoice_with_timestamp = str(invoice)
  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'VALORANT, BOOSTING FROM {rank_names[current_rank]} {division_names[current_division]} MARKS {marks} TO {rank_names[desired_rank]} {division_names[desired_division]}{boost_string}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})

def get_placement_order_result_by_rank(data):
  last_rank = data['last_rank']
  number_of_match = data['number_of_match']

  total_percent = 0
  
  duo_boosting = data['duo_boosting']
  select_booster = data['select_booster']
  turbo_boost = data['turbo_boost']
  streaming = data['streaming']
  select_champion = data['select_champion']
  champions_data = data['champion_data']

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

  if select_champion:
    total_percent += 0.0
    boost_options.append('CHOOSE AGENTS')
    select_champion_value = 1

  if promo_code != 'null':   
    try:
      promo_code_obj = PromoCode.objects.get(code=promo_code)
      promo_code_amount = promo_code_obj.discount_amount
      promo_code_id = promo_code_obj.pk
    except PromoCode.DoesNotExist:
      promo_code_amount = 0

  # Read data from utility function
  placement_data = get_valorant_placements_data()
  
  price = placement_data[last_rank] * number_of_match
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
    get_object_or_404(Booster, booster_id=booster_id, booster__is_booster=True, is_valo_player=True)
  else:
    booster_id = 0

  invoice = f'valo-2-P-{last_rank}-{number_of_match}-0-0-0-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{extend_order_id}-{server}-{price}-{select_champion_value}-{promo_code_id}-0-0-0-{champions_data}-{timezone.now()}'

  invoice_with_timestamp = str(invoice)
  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'VALORANT, BOOSTING OF {number_of_match} Start With {rank_names[last_rank]}{boost_string}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})







from gameBoosterss.order_info.orders import BaseOrderInfo, ChampionOrder, ExtendOrder
from gameBoosterss.order_info.division import DivisionGameOrderInfo
from gameBoosterss.order_info.placement import PlacementGameOrderInfo



class ValorantDOI(BaseOrderInfo, ChampionOrder, ExtendOrder, DivisionGameOrderInfo):
    division_prices_data = get_valorant_divisions_data()
    division_prices = [item for sublist in division_prices_data for item in sublist]
    division_prices.insert(0, 0)
    marks_data = get_valorant_marks_data()
    marks_data.insert(0, [0, 0, 0, 0, 0, 0])
    division_number = 3

class VlorantPOI(BaseOrderInfo, ChampionOrder, PlacementGameOrderInfo):
  placement_data = get_valorant_placements_data()