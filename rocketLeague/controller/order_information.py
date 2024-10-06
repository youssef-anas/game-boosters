from django.shortcuts import get_object_or_404
import json
from rocketLeague.models import *
from django.utils import timezone
from accounts.models import PromoCode
from booster.models import Booster
from rocketLeague.utils import (
    get_rocket_league_divisions_data,
    get_rocket_league_placements_data,
    get_rocket_league_seasonals_data,
    get_rocket_league_tournaments_data
)

division_names = ['','I','II','III']  
rank_names = ['UNRANK', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND', 'CHAMPION', 'GRAND CHAMPION', 'SUPERSONIC LEGEND']

# ---------------------------- Ranked ----------------------------
def get_division_order_result_by_rank(data):
  print('Data: ', data)
  # Division
  current_rank = data['current_rank']
  current_division = data['current_division']
  ranked_type = data['ranked_type']
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

  # Read data from utils file
  divisions_data = get_rocket_league_divisions_data()
  flattened_data = [item for sublist in divisions_data for item in sublist]
  flattened_data.insert(0, 0)

  start_division = ((current_rank-1) * 3) + current_division
  end_division = ((desired_rank-1) * 3)+ desired_division
  sublist = flattened_data[start_division:end_division ]
  total_sum = sum(sublist)
  price = total_sum 
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
    get_object_or_404(Booster, booster_id=booster_id, booster__is_booster=True, is_rl_player=True)
  else:
    booster_id = 0

  invoice = f'rl-9-D-{current_rank}-{current_division}-0-{desired_rank}-{desired_division}-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{extend_order_id}-{server}-{price}-0-{promo_code_id}-0-{ranked_type}-0-0-{timezone.now()}'

  invoice_with_timestamp = str(invoice)
  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'RL, BOOSTING FROM {rank_names[current_rank]} {division_names[current_division]} TO {rank_names[desired_rank]} {division_names[desired_division]}{boost_string}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})

# ---------------------------- Placement ----------------------------
def get_placement_order_result_by_rank(data):
  last_rank = data['last_rank']
  number_of_match = data['number_of_match']

  total_percent = 0

  duo_boosting = data['duo_boosting']
  select_booster = data['select_booster']
  turbo_boost = data['turbo_boost']
  streaming = data['streaming']

  extend_order_id = 0
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

  # Read data from JSON file
  placement_data = get_rocket_league_placements_data()
  
  price = placement_data[last_rank - 1] * number_of_match

  price += (price * total_percent)

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
    get_object_or_404(Booster, booster_id=booster_id, booster__is_booster=True, is_rl_player=True)
  else:
    booster_id = 0

  invoice = f'rl-9-P-{last_rank}-{number_of_match}-?-?-?-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{extend_order_id}-{server}-{price}-0-{promo_code_id}-0-0-0-0-{timezone.now()}'
  print('Invoice', invoice)

  invoice_with_timestamp = str(invoice)
  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'RL, BOOSTING OF {number_of_match} Start With {rank_names[last_rank]}{boost_string}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})

# ---------------------------- Seasonal ----------------------------
def get_seasonal_order_result_by_rank(data):
  current_rank = data['current_rank']
  number_of_wins = data['number_of_wins']

  total_percent = 0

  duo_boosting = data['duo_boosting']
  select_booster = data['select_booster']
  turbo_boost = data['turbo_boost']
  streaming = data['streaming']

  extend_order_id = 0
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

  seasonals_data = get_rocket_league_seasonals_data()
  
  price = seasonals_data[current_rank - 1] * number_of_wins

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
    get_object_or_404(Booster, booster_id=booster_id, booster__is_booster=True, is_rl_player=True)
  else:
    booster_id = 0


  invoice = f'rl-9-S-{current_rank}-{number_of_wins}-?-?-?-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{extend_order_id}-{server}-{price}-0-{promo_code_id}-0-0-0-0-{timezone.now()}'
  print('Invoice', invoice)

  invoice_with_timestamp = str(invoice)
  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'RL, BOOSTING OF {number_of_wins} Start With {rank_names[current_rank]}{boost_string}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})

# ---------------------------- Tournament ----------------------------
def get_tournament_order_result_by_rank(data):
  current_league = data['current_league']

  total_percent = 0

  duo_boosting = data['duo_boosting']
  select_booster = data['select_booster']
  turbo_boost = data['turbo_boost']
  streaming = data['streaming']

  extend_order_id = 0
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

  tournaments_data = get_rocket_league_tournaments_data()
  
  price = tournaments_data[current_league - 1]

  price += (price * total_percent)

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
    get_object_or_404(Booster, booster_id=booster_id, booster__is_booster=True, is_rl_player=True)
  else:
    booster_id = 0

  invoice = f'rl-9-T-{current_league}-{0}-?-?-?-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{extend_order_id}-{server}-{price}-0-{promo_code_id}-0-0-0-0-{timezone.now()}'
  print('Invoice', invoice)

  invoice_with_timestamp = str(invoice)
  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'RL, BOOSTING OF {0} Start With {rank_names[current_league]}{boost_string}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})

from gameBoosterss.order_info.orders import BaseOrderInfo, ExtendOrder
from gameBoosterss.order_info.division import DivisionGameOrderInfo
from gameBoosterss.order_info.placement import PlacementGameOrderInfo



class RL_DOI(BaseOrderInfo, ExtendOrder, DivisionGameOrderInfo):
    division_prices_data = get_rocket_league_divisions_data()
    division_prices = [item for sublist in division_prices_data for item in sublist]
    division_prices.insert(0, 0)
    marks_data = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    marks_data.insert(0, [0, 0, 0, 0, 0, 0])
    division_number = 3

    def get_game_info(self):
      super().get_game_info()
      self.game_order.update({'ranked_type': self.data['ranked_type']})
    
    def get_game_info_extended(self):
      super().get_game_info_extended()
      self.game_order.update({'ranked_type': self.extend_game.ranked_type})


class RL_POI(BaseOrderInfo, PlacementGameOrderInfo):
  placement_data = get_rocket_league_placements_data()

  def get_game_info(self):
    game_info_params = ['last_rank', 'number_of_match',]  
    # create a variable for each parameter
    for param in game_info_params:
        self.__setattr__(param, self.data[param])
    print(self.last_rank)
    self.game_order.update({'last_rank_id': self.last_rank})
    self.game_order.update({'number_of_match': self.number_of_match})

  def get_price(self):
    price = self.placement_data[self.last_rank-1] * self.number_of_match
    price = self.apply_extra_price(price)
    self.base_order.update({'price': price})
    self.extra_order.update({'price': price})
    return price
  

class RL_SOI(BaseOrderInfo, PlacementGameOrderInfo):
  placement_data = get_rocket_league_seasonals_data()

  def get_game_info(self):
    self.last_rank = self.data['current_rank']
    self.number_of_match = self.data['number_of_wins']
    self.game_order.update({'current_rank_id': self.last_rank})
    self.game_order.update({'number_of_wins': self.number_of_match})

  def get_price(self):
    price = self.placement_data[self.last_rank - 1] * self.number_of_match
    price = self.apply_extra_price(price)
    self.base_order.update({'price': price})
    self.extra_order.update({'price': price})
    return price

class RL_TOI(BaseOrderInfo, PlacementGameOrderInfo):
  placement_data = get_rocket_league_tournaments_data()

  def get_game_info(self):
    self.current_league = self.data['current_league']
    self.game_order.update({'current_league_id': self.current_league})

  def get_price(self):
    price = self.placement_data[self.current_league - 1]
    price = self.apply_extra_price(price)
    self.base_order.update({'price': price})
    self.extra_order.update({'price': price})
    return price