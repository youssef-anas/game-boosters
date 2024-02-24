from django.shortcuts import get_object_or_404
import json
from django.utils import timezone
from dota2.models import Dota2_50_MMR_Price, BaseOrder
from django.contrib.auth import get_user_model
User = get_user_model()

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


def get_rank_boost_order_result_by_rank(data,extend_order_id):
  print('Data: ', data)
  # Division
  current_MMR = data['current_MMR']
  desired_MMR = data['desired_MMR']

  total_percent = 0
  duo_boosting = data['duo_boosting']
  select_booster = data['select_booster']
  turbo_boost = data['turbo_boost']
  streaming = data['streaming']
  choose_agents = data['choose_agents']
  role = data['role']

  duo_boosting_value = 0
  select_booster_value = 0
  turbo_boost_value = 0
  streaming_value = 0
  choose_agents_value = 0

  boost_options = []

  if duo_boosting:
    total_percent += 0.65
    boost_options.append('DUO BOOSTING')
    duo_boosting_value = 1

  if select_booster:
    total_percent += 0.05
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

  if choose_agents:
    total_percent += 0.0
    boost_options.append('CHOOSE AGENTS')
    choose_agents_value = 1
      
  dota_50_MMR_Price = Dota2_50_MMR_Price.objects.all().first().price
  total_sum = (desired_MMR - current_MMR) * (dota_50_MMR_Price * 50)
  price = total_sum + (total_sum * total_percent)
  price = round(price, 2)
  print('Price', price)

  if extend_order_id > 0:
    try:
      extend_order = BaseOrder.objects.get(id=extend_order_id)
      extend_order_price = extend_order.price
      price = round((price - extend_order_price), 2)
      print('Price', price)
    except:
      pass

  booster_id = data['choose_booster']
  if booster_id > 0 :
    get_object_or_404(User,id=booster_id,is_booster=True)
  else:
    booster_id = 0

  if current_MMR >= 0 and current_MMR <= 769 :
    current_rank = rank_names[1] # Herald 
  elif current_MMR >= 770 and current_MMR <= 1539:
    current_rank = rank_names[2] # Guardian 
  elif current_MMR >= 1540 and current_MMR <= 2309:
    current_rank = rank_names[3] # Crusader 
  elif current_MMR >= 2310 and current_MMR <= 3079:
    current_rank = rank_names[4] # Archon 
  elif current_MMR >= 3080 and current_MMR <= 3849:
    current_rank = rank_names[5] # Legend 
  elif current_MMR >= 3850 and current_MMR <= 4619:
    current_rank = rank_names[6] # Ancient 
  elif current_MMR >= 4620 and current_MMR <= 5420:
    current_rank = rank_names[7] # Divine 
  elif current_MMR >= 5421:
    current_rank = rank_names[8] # Immortal 
  else:
    current_rank = rank_names[0]
  
  if desired_MMR >= 0 and desired_MMR <= 769 :
    desired_rank = rank_names[1] # Herald 
  elif desired_MMR >= 770 and desired_MMR <= 1539:
    desired_rank = rank_names[2] # Guardian 
  elif desired_MMR >= 1540 and desired_MMR <= 2309:
    desired_rank = rank_names[3] # Crusader 
  elif desired_MMR >= 2310 and desired_MMR <= 3079:
    desired_rank = rank_names[4] # Archon 
  elif desired_MMR >= 3080 and desired_MMR <= 3849:
    desired_rank = rank_names[5] # Legend 
  elif desired_MMR >= 3850 and desired_MMR <= 4619:
    desired_rank = rank_names[6] # Ancient 
  elif desired_MMR >= 4620 and desired_MMR <= 5420:
    desired_rank = rank_names[7] # Divine 
  elif desired_MMR >= 5421:
    desired_rank = rank_names[8] # Immortal 
  else:
    desired_rank = rank_names[0]
  
  
  invoice = f'WOW-6-A-{current_rank}-{current_MMR}-0-{desired_rank}-{desired_MMR}-{duo_boosting_value}-{select_booster_value}-{turbo_boost_value}-{streaming_value}-{booster_id}-{price}-{extend_order_id}-{timezone.now()}-A-{choose_agents_value}-{role}'
  print('Invoice', invoice)

  invoice_with_timestamp = str(invoice)
  boost_string = " WITH " + " AND ".join(boost_options) if boost_options else ""
  name = f'WOW, BOOSTING FROM {rank_names[current_rank]} {current_MMR} TO {rank_names[desired_rank]} {desired_MMR}{boost_string} ROLE: {role_names[role]}'

  return({'name':name,'price':price,'invoice':invoice_with_timestamp})