from django.shortcuts import get_object_or_404
import json
from django.utils import timezone
from WorldOfWarcraft.models import  BaseOrder
from accounts.models import PromoCode
from booster.models import Booster
from WorldOfWarcraft.models import WorldOfWarcraftRpsPrice, WorldOfWarcraftBoss, WorldOfWarcraftBundle
from WorldOfWarcraft.utils import extract_bosses_ids, extract_bundle_id, get_keyston_price, get_level_up_price
from django.db.models import Sum

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


from gameBoosterss.order_info.levelup import LevelupGameOrderInfo
from gameBoosterss.order_info.arena import ArenaGameOrderInfo
from gameBoosterss.order_info.orders import BaseOrderInfo, ExtendOrder
from gameBoosterss.order_info.wow import RaidSimpleGameOrderInfo, RaidBundleGameOrderInfo, DungeonSimpleGameOrderInfo

class WOW_AOI(BaseOrderInfo, ExtendOrder, ArenaGameOrderInfo):
  points_value = 50
  
  def get_percent_price(self):
    return {
        'turbo_boost': 20,
        'streaming': 15,
    }

  def get_arena_price_price(self):
    prices = WorldOfWarcraftRpsPrice.objects.all().first()
    self.game_order.update({'is_arena_2vs2': self.data['is_arena_2vs2']})
    if self.data['is_arena_2vs2'] == True:
      return prices.price_of_2vs2
    else:
      return prices.price_of_3vs3
    
  def get_totla_percent_price(self):
    super().get_totla_percent_price()
    extra_percent_price = {
      'rank1_player': 40,
      'tournament_player': 100,
      }
    for key, value in extra_percent_price.items():
      if self.data[key]:
        self.total_percent += value
        self.game_order[key] = self.data[key]
    if self.data['boost_method'] == 'remote-control':  
      self.total_percent += 30
    self.game_order.update({'boost_method': self.data['boost_method']})

class WOW_LOI (BaseOrderInfo, LevelupGameOrderInfo):
  faceit_prices = get_level_up_price()

  def get_percent_price(self):
    return {
        'turbo_boost': 20,
        'streaming': 15,
    }

  def get_totla_percent_price(self):
    super().get_totla_percent_price()
    # if self.data['boost_method'] == 'remote-control':  
    #   self.total_percent += 30
    # self.game_order.update({'boost_method': self.data['boost_method']})

  def get_price(self):
    level_number = self.desired_level - self.current_level 
    price = level_number * self.faceit_prices
    price = self.apply_extra_price(price)
    price_for_payment = round(price - self.extend_order_price, 2)
    self.base_order.update({'price': price})
    self.extra_order.update({'price': price_for_payment})
    return price  


class WOW_RSOI(BaseOrderInfo, RaidSimpleGameOrderInfo):
  def get_percent_price(self):
    return {
        'turbo_boost': 20,
        'streaming': 15,
    }

class WOW_RBOI(BaseOrderInfo, RaidBundleGameOrderInfo):  
  def get_percent_price(self):
    return {
        'turbo_boost': 20,
        'streaming': 15,
    }
  
class WOW_DSOI(BaseOrderInfo, DungeonSimpleGameOrderInfo):  
  def get_percent_price(self):
    return {
        'turbo_boost': 20,
        'streaming': 15,
    }