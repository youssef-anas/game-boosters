from django.shortcuts import get_object_or_404
import json
from django.utils import timezone
from dota2.models import Dota2MmrPrice, BaseOrder
from accounts.models import PromoCode
from booster.models import Booster

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

prices = None
with open('static/dota2/data/prices.json', 'r') as file:
  prices = json.load(file)

def get_rank_boost_order_result_by_rank(data,extend_order_id):
  MIN_DESIRED_VALUE = 50
  # Division
  division_price = prices['division']

  def get_price(currentMmr, desiredMmr):
    def get_range(mmr):
      if mmr <= 2000: return division_price[0]
      if mmr <= 3000: return division_price[1]
      if mmr <= 4000: return division_price[2]
      if mmr <= 5000: return division_price[3]
      if mmr <= 5500: return division_price[4]
      if mmr <= 6000: return division_price[5]
      if mmr > 6000: return  division_price[6]

    currentRange = get_range(currentMmr)
    desiredRange = get_range(desiredMmr)

    if currentRange == desiredRange: return currentRange
    else: (desiredRange + currentRange) / 2

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
  
  MIN_PRICE = get_price(current_division, desired_division)

  price = (desired_division - current_division) * (MIN_PRICE / MIN_DESIRED_VALUE)

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
  
  invoice = f'DOTA2-10-A-{current_rank}-{current_division}-0-{desired_rank}-{desired_division}-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{extend_order_id}-{server}-{price}-{select_champion_value}-{promo_code_id}-{role}-0-0-{timezone.now()}'
  
  invoice_with_timestamp = str(invoice)

  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'DOTA2, BOOSTING FROM {rank_names[current_rank]} {current_division} TO {rank_names[desired_rank]} {desired_division}{boost_string} ROLE: {role_names[role]}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})

def get_palcement_order_result_by_rank(data,extend_order_id):
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
  select_champion = data['select_champion']

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
   
  placement_price = price['placement']

  price = placement_price[last_rank - 1] * number_of_match
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
    get_object_or_404(Booster, booster_id=booster_id, booster__is_booster=True, is_dota2_player=True)
  else:
    booster_id = 0

  invoice = f'DOTA2-10-P-{last_rank}-{number_of_match}-{last_division}-none-none-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{extend_order_id}-{server}-{price}-{select_champion_value}-{promo_code_id}-{role}-0-0-{timezone.now()}'

  invoice_with_timestamp = str(invoice)

  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'DOTA2, BOOSTING OF {number_of_match} Start With {rank_names[last_rank]}{boost_string}  ROLE: {role_names[role]}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})