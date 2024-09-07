from django.shortcuts import get_object_or_404
import json
from django.utils import timezone
from WorldOfWarcraft.models import  BaseOrder
from accounts.models import PromoCode
from booster.models import Booster
from WorldOfWarcraft.models import WorldOfWarcraftRpsPrice, WorldOfWarcraftBoss, WorldOfWarcraftBundle
from WorldOfWarcraft.utils import extract_bosses_ids, extract_bundle_id, get_keyston_price, get_level_up_price
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

  rank1_player = data['rank1_player']
  tournament_player = data['tournament_player']
  boost_method = data['boost_method']
  turbo_boost = data['turbo_boost']
  streaming = data['streaming']

  server = data['server']
  promo_code = data['promo_code']
  promo_code_id = 0

  duo_boosting_value = 0
  select_booster_value = 0
  turbo_boost_value = 0
  streaming_value = 0

  rank1_player_value = 0
  tournament_player_value = 0

  is_arena_2vs2_value= 0

  promo_code_amount = 0

  boost_options = []

  if rank1_player:
    total_percent += 0.40
    boost_options.append('RANK 1 BOOSTING')
    rank1_player_value = 1

  if tournament_player:
    total_percent += 1.00
    boost_options.append('TOURNAMENT BOOSTING')
    tournament_player_value = 1  

  if boost_method == 'remote-control':
    total_percent += 0.30  

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

  booster_id = 0
  if booster_id > 0 :
    get_object_or_404(Booster, booster_id=booster_id, booster__is_booster=True, is_wow_player=True)
  else:
    booster_id = 0

  invoice = f'WOW-6-A-{current_rank}-{current_RP}-0-{desired_rank}-{desired_RP}-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{extend_order_id}-{server}-{price}-0-{promo_code_id}-0-0-{is_arena_2vs2_value}-0-{rank1_player_value}-{tournament_player_value}-{boost_method}-{timezone.now()}'

  invoice_with_timestamp = str(invoice)
  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'WOW, BOOSTING FROM {rank_names[current_rank]} {current_RP} TO {rank_names[desired_rank]} {desired_RP}{boost_string}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})



def get_raid_simple_price_by_bosses(data):
  map_name = data['map']
  bosses = data['bosses']
  difficulty_chosen = data['difficulty_chosen']
  boost_method = data['boost_method']
  loot_priority = data['loot_priority']


  if map_name == 'incarnates':
    map = 1

  if map_name == 'crucible':
    map = 2

  if map_name == 'amirdrassil':
    map = 3    

  bosses_ids = extract_bosses_ids(bosses)
  base_bosses = WorldOfWarcraftBoss.objects.filter(map=map)

  select_bosses = base_bosses.filter(id__in=bosses_ids).order_by('id')

  if select_bosses:
    total_bosses_price = select_bosses.aggregate(Sum('price'))['price__sum']
  else:
    total_bosses_price = 0

  


  total_percent = 0

  turbo_boost = data['turbo_boost']
  streaming = data['streaming']

  server = data['server']
  promo_code = data['promo_code']
  promo_code_id = 0

  duo_boosting_value = 0
  select_booster_value = 0
  turbo_boost_value = 0
  streaming_value = 0
  loot_priority_value = 0

  promo_code_amount = 0

  boost_options = []


  if boost_method == 'remote-control':
    total_percent += 0.30  
    boost_options.append('REMOTE CONTROL')

  if loot_priority:
    total_percent += 0.50  
    loot_priority_value = 1
    boost_options.append('LOOT PRIORITY')
  

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



  booster_id = 0
  if booster_id > 0 :
    get_object_or_404(Booster, booster_id=booster_id, booster__is_booster=True, is_wow_player=True)
  else:
    booster_id = 0

  invoice = f'WOW-6-R-{map}-{bosses_ids}-{difficulty_chosen}-{0}-{0}-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{0}-{server}-{price}-0-{promo_code_id}-0-0-{0}-0-{loot_priority_value}-{boost_method}-{timezone.now()}'

  invoice_with_timestamp = str(invoice)
  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'WOW, BOOSTING {boost_string}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})



def get_raid_bundle_order_info(data):
  bundle_id = data['bundle_id']
  bundle_obj = get_object_or_404(WorldOfWarcraftBundle, pk=bundle_id)
  bundle_price = bundle_obj.price

  total_percent = 0

  turbo_boost = data['turbo_boost']
  streaming = data['streaming']

  loot_priority = data['loot_priority']
  boost_method = data['boost_method']

  server = data['server']
  promo_code = data['promo_code']
  promo_code_id = 0

  duo_boosting_value = 0
  select_booster_value = 0
  turbo_boost_value = 0
  streaming_value = 0
  loot_priority_value = 0


  promo_code_amount = 0

  boost_options = []


  if boost_method == 'remote-control':
    boost_options.append('REMOTE CONTROL')
    total_percent += 0.30  

  if loot_priority:
    total_percent += 0.50  
    loot_priority_value = 1
    boost_options.append('LOOT PRIORITY')

  if turbo_boost:
    total_percent += 0.20
    boost_options.append('TURBO BOOSTING')
    turbo_boost_value = 1
  
  if streaming:
    total_percent += 0.15
    boost_options.append('STREAMING')
    streaming_value = 1

  if promo_code != 'null':   
    try:
      promo_code_obj = PromoCode.objects.get(code=promo_code)
      promo_code_amount = promo_code_obj.discount_amount
      promo_code_id = promo_code_obj.pk
    except PromoCode.DoesNotExist:
      promo_code_amount = 0
  
  price = bundle_price
  price += (price * total_percent)
  price -= price * (promo_code_amount/100)
  price = round(price, 2)



  booster_id = 0
  if booster_id > 0 :
    get_object_or_404(Booster, booster_id=booster_id, booster__is_booster=True, is_wow_player=True)
  else:
    booster_id = 0

  invoice = f'WOW-6-RB-{bundle_id}-{loot_priority_value}-{0}-{0}-{0}-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{0}-{server}-{price}-0-{promo_code_id}-0-0-{0}-0-{boost_method}-{timezone.now()}'

  invoice_with_timestamp = str(invoice)
  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'WOW, BOOSTING {bundle_obj.name} {boost_string}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})




def get_dungeon_order_info(data):
  keystone = data['keystone']
  keys = data['keys']

  map_preferred = data['map_preferred']

  # maps 
  algathar_academy = data['algathar_academy']
  azure_vault = data['azure_vault']
  brackenhide_hollow = data['brackenhide_hollow']
  halls_of_infusion = data['halls_of_infusion']
  neltharus = data['neltharus']
  nokhud_offensive = data['nokhud_offensive']
  ruby_life_pools = data['ruby_life_pools']
  uldaman_legacy_of_tyr = data['uldaman_legacy_of_tyr']

  # Traders
  trader = data['traders']
  traders_armor_type = data['traders_armor_type']


  keyston_price = get_keyston_price()
  

  kayestoneWithKaysPrice = keys * keyston_price[keystone]


  total_percent = 0


  turbo_boost = data['turbo_boost']
  streaming = data['streaming']
  boost_method = data['boost_method']
  timed = data['timed']

  server = data['server']
  promo_code = data['promo_code']
  promo_code_id = 0

  duo_boosting_value = 0
  select_booster_value = 0
  turbo_boost_value = 0
  streaming_value = 0

  timed_value = 0
  


  promo_code_amount = 0

  boost_options = []


  if boost_method == 'remote-control':
    boost_options.append('REMOTE CONTROL')
    total_percent += 0.30  

  if timed:
    total_percent += 0.20  
    timed_value = 1
    boost_options.append('TIMED BOOSTING')

  if turbo_boost:
    total_percent += 0.20
    boost_options.append('TURBO BOOSTING')
    turbo_boost_value = 1
  
  if streaming:
    total_percent += 0.15
    boost_options.append('STREAMING')
    streaming_value = 1

  if map_preferred == 'Specific':
    total_percent += 0.05

  if trader == '1 trader':
    total_percent += 0.15
  elif trader == '2 trader':
    total_percent += 0.30
  elif trader == '3 trader':
    total_percent += 0.40  
  elif trader == 'full-Priority':
    total_percent += 0.50  
    trader = "full_Priority"      


  if promo_code != 'null':   
    try:
      promo_code_obj = PromoCode.objects.get(code=promo_code)
      promo_code_amount = promo_code_obj.discount_amount
      promo_code_id = promo_code_obj.pk
    except PromoCode.DoesNotExist:
      promo_code_amount = 0
  
  price = kayestoneWithKaysPrice
  price += (price * total_percent)
  price -= price * (promo_code_amount/100)
  price = round(price, 2)



  booster_id = 0
  if booster_id > 0 :
    get_object_or_404(Booster, booster_id=booster_id, booster__is_booster=True, is_wow_player=True)
  else:
    booster_id = 0

  maps = {
    'algathar_academy': algathar_academy,
    'azure_vault': azure_vault,
    'brackenhide_hollow': brackenhide_hollow,
    'halls_of_infusion': halls_of_infusion,
    'neltharus': neltharus,
    'nokhud_offensive': nokhud_offensive,
    'ruby_life_pools': ruby_life_pools,
    'uldaman_legacy_of_tyr': uldaman_legacy_of_tyr
  }  

  invoice = f'WOW-6-DS-{keystone}-{keys}-{map_preferred}-{trader}-{traders_armor_type}-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{0}-{server}-{price}-0-{promo_code_id}-0-0-{maps}-0-{timed_value}-{boost_method}-{timezone.now()}'

  invoice_with_timestamp = str(invoice)
  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'WOW, BOOSTING {boost_string}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})


def get_level_up_price_form_serilaizer(data):

  current_level = data['current_level']
  desired_level = data['desired_level']

  promo_code = data['promo_code']
  streaming = data['streaming']
  turbo_boost = data['turbo_boost']
  server = data['server']

  level_price = get_level_up_price()


  number_of_level = desired_level - current_level
  Full_level_prices = number_of_level * level_price


  total_percent = 0

  promo_code_amount = 0

  boost_options = []

  streaming_value = 0
  turbo_boost_value = 0
  promo_code_id = 0

  if turbo_boost:
    total_percent += 0.20
    boost_options.append('TURBO BOOSTING')
    turbo_boost_value = 1
  
  if streaming:
    total_percent += 0.15
    boost_options.append('STREAMING')
    streaming_value = 1


  if promo_code != 'null':   
    try:
      promo_code_obj = PromoCode.objects.get(code=promo_code)
      promo_code_amount = promo_code_obj.discount_amount
      promo_code_id = promo_code_obj.pk
    except PromoCode.DoesNotExist:
      promo_code_amount = 0
  
  price = Full_level_prices
  price += (price * total_percent)
  price -= price * (promo_code_amount/100)
  price = round(price, 2)
  
  invoice = f'WOW-6-F-{current_level}-{0}-{0}-{desired_level}-{0}-{0}-{0}-{turbo_boost_value}-{streaming_value}-{0}-{0}-{server}-{price}-{0}-{promo_code_id}-0-0-0-0-{timezone.now()}'

  invoice_with_timestamp = str(invoice)
  
  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'WOW, BOOSTING FROM {current_level} Level TO {desired_level} Level {boost_string}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})

