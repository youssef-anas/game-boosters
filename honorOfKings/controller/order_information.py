from django.shortcuts import get_object_or_404
from wildRift.models import *
from django.utils import timezone
from accounts.models import PromoCode
from booster.models import Booster
from honorOfKings.utils import get_hok_divisions_data, get_hok_marks_data

division_names = ['','V','IV','III','II','I']
rank_names = ['UNRANK', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND', 'KING']

def get_division_order_result_by_rank(data):
  print('Data: ', data)
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

  extend_order_id = data['extend_order']
  server = data['server']
  promo_code = data['promo_code']
  promo_code_id = 0

  duo_boosting_value = 0
  select_booster_value = 0
  turbo_boost_value = 0
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
  
  if streaming:
    total_percent += 0.15
    boost_options.append('STREAMING')
    streaming_value = 1

  if turbo_boost:
    total_percent += 0.20
    boost_options.append('TURBO BOOSTING')
    turbo_boost_value = 1

  if promo_code != 'null':   
    try:
      promo_code_obj = PromoCode.objects.get(code=promo_code)
      promo_code_amount = promo_code_obj.discount_amount
      promo_code_id = promo_code_obj.pk
    except PromoCode.DoesNotExist:
      promo_code_amount = 0

  # Read data from utils file
  division_price = get_hok_divisions_data()
  flattened_data = [item for sublist in division_price for item in sublist]
  flattened_data.insert(0,0)
  ##
  marks_data = get_hok_marks_data()
  marks_data.insert(0,[0,0,0,0])
  ##    
  start_division = ((current_rank-1) * 5) + current_division
  end_division = ((desired_rank-1) * 5) + desired_division
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
    get_object_or_404(Booster, booster_id=booster_id, booster__is_booster=True, is_hok_player=True)
  else:
    booster_id = 0

  invoice = f'HOK-11-D-{current_rank}-{current_division}-{marks}-{desired_rank}-{desired_division}-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{extend_order_id}-{server}-{price}-0-{promo_code_id}-0-0-0-0-{timezone.now()}'

  invoice_with_timestamp = str(invoice)
  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'HOK, BOOSTING FROM {rank_names[current_rank]} {division_names[current_division]} MARKS {marks} TO {rank_names[desired_rank]} {division_names[desired_division]}{boost_string}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})

from gameBoosterss.order_info.orders import BaseOrderInfo, ExtendOrder
from gameBoosterss.order_info.division import DivisionGameOrderInfo

class HOK_DOI(BaseOrderInfo, DivisionGameOrderInfo, ExtendOrder):
  division_prices_data = get_hok_divisions_data()
  division_prices = [item for sublist in division_prices_data for item in sublist]
  division_prices.insert(0, 0)
  marks_data = get_hok_marks_data()
  marks_data.insert(0, [0, 0, 0, 0, 0, 0])
  division_number = 5