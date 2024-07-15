from django.shortcuts import get_object_or_404
import json
from django.utils import timezone
from WorldOfWarcraft.models import  BaseOrder
from accounts.models import PromoCode
from booster.models import Booster
from WorldOfWarcraft.models import WorldOfWarcraftRpsPrice, WorldOfWarcraftBoss
from WorldOfWarcraft.utils import extract_ids
from django.db.models import Sum

rank_names = ['UNRANK', '0-1599', '1600-1799', '1800-2099', '2100-2500']

def get_arena_order_result_by_rank(data,extend_order_id):
  # Prices
  prices = WorldOfWarcraftRpsPrice.objects.all().first()
  price_of_2vs2 = prices.price_of_2vs2
  price_of_3vs3 = prices.price_of_3vs3

  # Ranks
  current_rank = data['current_rank']
  desired_rank = data['desired_rank']

  # Division
  current_RP = data['current_RP']
  desired_RP = data['desired_RP']

  # Is 2vs2
  is_arena_2vs2 = data['is_arena_2vs2']

  total_percent = 0

  duo_boosting = data['duo_boosting']
  select_booster = data['select_booster']
  turbo_boost = data['turbo_boost']
  streaming = data['streaming']

  server = data['server']
  promo_code = data['promo_code']
  promo_code_id = 0

  duo_boosting_value = 0
  select_booster_value = 0
  turbo_boost_value = 0
  streaming_value = 0

  is_arena_2vs2_value= 0

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

  if is_arena_2vs2:
    is_arena_2vs2_value = 1

  if promo_code != 'null':   
    try:
      promo_code_obj = PromoCode.objects.get(code=promo_code)
      promo_code_amount = promo_code_obj.discount_amount
      promo_code_id = promo_code_obj.pk
    except PromoCode.DoesNotExist:
      promo_code_amount = 0
      
  if is_arena_2vs2:
    price = (desired_RP - current_RP) * (price_of_2vs2 / 50)
  else: 
    price = (desired_RP - current_RP) * (price_of_3vs3 / 50)

  price += (price * total_percent)
  price -= price * (promo_code_amount/100)
  price = round(price, 2)

  if extend_order_id > 0:
    try:
      extend_order = BaseOrder.objects.get(id=extend_order_id)
      extend_order_price = extend_order.price
      price = round((price - extend_order_price), 2)
    except:
      pass

  booster_id = data['choose_booster']
  if booster_id > 0 :
    get_object_or_404(Booster, booster_id=booster_id, booster__is_booster=True, is_wow_player=True)
  else:
    booster_id = 0

  invoice = f'WOW-6-A-{current_rank}-{current_RP}-0-{desired_rank}-{desired_RP}-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{extend_order_id}-{server}-{price}-0-{promo_code_id}-0-0-{is_arena_2vs2_value}-0-{timezone.now()}'

  invoice_with_timestamp = str(invoice)
  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'WOW, BOOSTING FROM {rank_names[current_rank]} {current_RP} TO {rank_names[desired_rank]} {desired_RP}{boost_string}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})



def get_raid_simple_price_by_bosses(data):
  map_name = data['map']
  bosses = data['bosses']
  difficulty_chosen = data['difficulty_chosen']


  if map_name == 'incarnates':
    map = 1

  if map_name == 'crucible':
    map = 2

  if map_name == 'amirdrassil':
    map = 3    

  bosses_ids = extract_ids(bosses)
  base_bosses = WorldOfWarcraftBoss.objects.filter(map=map)

  select_bosses = base_bosses.filter(id__in=bosses_ids).order_by('id')
  if select_bosses:
    total_bosses_price = select_bosses.aggregate(Sum('price'))['price__sum']
  else:
    total_bosses_price = 0

  


  total_percent = 0

  duo_boosting = data['duo_boosting']
  select_booster = data['select_booster']
  turbo_boost = data['turbo_boost']
  streaming = data['streaming']

  server = data['server']
  promo_code = data['promo_code']
  promo_code_id = 0

  duo_boosting_value = 0
  select_booster_value = 0
  turbo_boost_value = 0
  streaming_value = 0

  is_arena_2vs2_value= 0

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

  if difficulty_chosen in [0.3, 0.4, 0.5]:
    total_percent += difficulty_chosen
    

  if promo_code != 'null':   
    try:
      promo_code_obj = PromoCode.objects.get(code=promo_code)
      promo_code_amount = promo_code_obj.discount_amount
      promo_code_id = promo_code_obj.pk
    except PromoCode.DoesNotExist:
      promo_code_amount = 0
  
  price = total_bosses_price
  price += (price * total_percent)
  price -= price * (promo_code_amount/100)
  price = round(price, 2)



  booster_id = data['choose_booster']
  if booster_id > 0 :
    get_object_or_404(Booster, booster_id=booster_id, booster__is_booster=True, is_wow_player=True)
  else:
    booster_id = 0

  invoice = f'WOW-6-R-{map}-{bosses_ids}-{difficulty_chosen}-{0}-{0}-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{0}-{server}-{price}-0-{promo_code_id}-0-0-{0}-0-{timezone.now()}'

  invoice_with_timestamp = str(invoice)
  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'WOW, BOOSTING FROM {boost_string}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})