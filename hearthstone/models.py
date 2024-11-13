from django.db import models
from accounts.models import BaseOrder, Wallet, PromoCode
from accounts.templatetags.custom_filters import ten_romanize_division,romanize_division
import requests
import math

# Create your models here.
class HearthstoneRank(models.Model):
  rank_name = models.CharField(max_length=25)
  rank_image = models.ImageField(upload_to='hearthstone/images/', blank=True, null=True)

  def __str__(self):
    return self.rank_name
    
  def get_image_url(self):
    return self.rank_image.url
  
class HearthstoneTier(models.Model):
  rank = models.OneToOneField('HearthstoneRank', related_name='tier', on_delete=models.CASCADE)
  from_X_to_IX = models.FloatField(default=0)
  from_IX_to_VIII = models.FloatField(default=0)
  from_VIII_to_VII = models.FloatField(default=0)
  from_VII_to_VI = models.FloatField(default=0)
  from_VI_to_V = models.FloatField(default=0)
  from_V_to_IV = models.FloatField(default=0)
  from_IV_to_III = models.FloatField(default=0)
  from_III_to_II = models.FloatField(default=0)
  from_II_to_I = models.FloatField(default=0)
  from_I_to_IV_next = models.FloatField(default=0)

  def __str__(self):
    return f"Tiers for {self.rank.rank_name}"

class HearthstoneMark(models.Model):
  rank = models.OneToOneField('HearthstoneRank', related_name='mark', on_delete=models.CASCADE)
  marks_3 = models.FloatField(default=0)
  marks_2 = models.FloatField(default=0)
  marks_1 = models.FloatField(default=0)

  def __str__(self):
    return f"{self.rank} -> Marks 3: {self.marks_3}, Marks 2 : {self.marks_2}, Marks 1 : {self.marks_1}"
  

class HearthstoneBattle(models.Model):
  rank_name = models.CharField(max_length=25)
  rank_image = models.ImageField(upload_to='hearthstone/images/', blank=True, null=True)

  def __str__(self):
    return self.rank_name
    
  def get_image_url(self):
    return self.rank_image.url
  
class HearthstoneBattlePrice(models.Model):  
  from_0_to_2000 = models.FloatField(default=0)
  from_2000_to_4000 = models.FloatField(default=0)
  from_4000_to_6000 = models.FloatField(default=0)
  from_6000_to_8000 = models.FloatField(default=0)
  from_8000_to_10000 = models.FloatField(default=0)

  def __str__(self):
    return f"Battle prices"

def get_hearthstone_divisions_data():
  divisions = HearthstoneTier.objects.all().order_by('id')
  divisions_data = [
      [division.from_X_to_IX, division.from_IX_to_VIII, division.from_VIII_to_VII, division.from_VII_to_VI, division.from_VI_to_V, division.from_V_to_IV, division.from_IV_to_III, division.from_III_to_II, division.from_II_to_I, division.from_I_to_IV_next]
      for division in divisions
  ]
  return divisions_data

def get_hearthstone_marks_data():
  marks = HearthstoneMark.objects.all().order_by('id')
  marks_data = [
      [0, mark.marks_3, mark.marks_2, mark.marks_1]
      for mark in marks
  ]
  return marks_data

def get_hearthstone_battle_prices():
    price = HearthstoneBattlePrice.objects.all().first()
    battle_prices_data = [
        price.from_0_to_2000, 
        price.from_2000_to_4000,
        price.from_4000_to_6000,
        price.from_6000_to_8000,
        price.from_8000_to_10000
    ]
    return battle_prices_data



class HearthstoneDivisionOrder(models.Model):
  DIVISION_CHOICES = [
    (1, 'X'),
    (2, 'IX'),
    (3, 'VIII'),
    (4, 'VII'),
    (5, 'VI'),
    (6, 'V'),
    (7, 'IV'),
    (8, 'III'),
    (9, 'II'),
    (10, 'I'),
  ]
  MARKS_CHOISES = [
    (0, '0 Stars'),
    (1, '3 Stars'),
    (2, '2 Stars'),
    (3, '1 Stars'),
  ]
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='hearthstone_division_order')
  current_rank = models.ForeignKey(HearthstoneRank, on_delete=models.CASCADE, default=None, related_name='current_rank',blank=True, null=True)
  reached_rank = models.ForeignKey(HearthstoneRank, on_delete=models.CASCADE, default=None, related_name='reached_rank',blank=True, null=True)
  desired_rank = models.ForeignKey(HearthstoneRank, on_delete=models.CASCADE, default=None, related_name='desired_rank',blank=True, null=True)
  current_division = models.PositiveSmallIntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  reached_division = models.PositiveSmallIntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  desired_division = models.PositiveSmallIntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  current_marks = models.PositiveSmallIntegerField(choices=MARKS_CHOISES,blank=True, null=True)
  reached_marks = models.PositiveSmallIntegerField(choices=MARKS_CHOISES,blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add =True)
  updated_at = models.DateTimeField(auto_now =True)

  # select_champion = models.BooleanField(default=True, blank=True, null=True)

  def send_discord_notification(self):
    if self.order.status == 'Extend':
        return print('Extend Order')
    discord_webhook_url = 'https://discordapp.com/api/webhooks/1209758608599031858/PtdjMTcZq9dR5lo9uTVX-cJPSPEduMXcUjoiQrMchDHvyHv0oTuZnCIVIcsX6dwqGCy3'
    current_time = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    embed = {
        "title": "Hearth Stone",
        "description": (
            f"**Order ID:** {self.order.name}\n"
            f" From {str(self.current_rank).upper()} {romanize_division(self.current_division)} Marks {self.current_marks} "
            f" To {str(self.desired_rank).upper()} {romanize_division(self.desired_division)}\n server {self.order.customer_server}"
        ),
        "color": 0x3498db,  # Hex color code for a Discord blue color
        "footer": {"text": f"{current_time}"}, 
    }
    data = {
        "content": "New order has arrived \n",  # Set content to a space if you only want to send an embed
        "embeds": [embed],
    }


    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(discord_webhook_url, json=data, headers=headers)

    if response.status_code != 204:
        print(f"Failed to send Discord notification. Status code: {response.status_code}")


  def save_with_processing(self, *args, **kwargs):
    self.order.game_id = 7
    self.order.game_type = 'D'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'HS{self.order.id}'
    self.order.update_actual_price()
    self.order.save()
    super().save(*args, **kwargs)
    self.send_discord_notification()
    
  def get_details(self):
    return f"From {str(self.current_rank).upper()} {ten_romanize_division(self.current_division)} {'0' if self.current_marks == 0 else ('3' if self.current_marks == 1 else ('2' if self.current_marks == 2 else '1'))} STAR To {str(self.desired_rank).upper()} {ten_romanize_division(self.desired_division)}"

  def __str__(self):
    return self.get_details()
  
  def get_rank_value(self, *args, **kwargs):
    promo_code = f'{None},{None}'

    if self.order.promo_code != None:
      promo_code = f'{self.order.promo_code.code},{self.order.promo_code.discount_amount}'

    return f"{self.current_rank.pk},{self.current_division},{self.current_marks},{self.desired_rank.pk},{self.desired_division},{self.order.duo_boosting},{self.order.select_booster},{self.order.turbo_boost},{self.order.streaming},{0},{self.order.customer_server},{promo_code},1"

  def get_order_price(self):
    # Read data from utils file
    division_price = get_hearthstone_divisions_data()
    flattened_data = [item for sublist in division_price for item in sublist]
    flattened_data.insert(0,0)
    ##
    
    marks_data = get_hearthstone_marks_data()
    marks_data.insert(0,[0,0,0])
  ##  
          
    try:
      promo_code_amount = self.order.promo_code.discount_amount
    except:
      promo_code_amount = 0

    current_rank = self.current_rank.id
    reached_rank = self.reached_rank.id

    current_division = self.current_division
    reached_division = self.reached_division

    current_marks = self.current_marks
    reached_marks = self.reached_marks

    total_percent = 0

    if self.order.duo_boosting:
      total_percent += 0.65

    if self.order.select_booster:
      total_percent += 0.10

    if self.order.turbo_boost:
      total_percent += 0.20

    if self.order.streaming:
      total_percent += 0.15

    start_division = ((current_rank-1) * 10) + current_division
    end_division = ((reached_rank-1) * 10)+ reached_division
    marks_price = marks_data[current_rank][current_marks]
    marks_price_reached = 0
    marks_price_reached = marks_data[reached_rank][reached_marks]

    sublist = flattened_data[start_division:end_division]


    total_sum = sum(sublist)    


    custom_price = total_sum - marks_price + marks_price_reached
    
    custom_price += (custom_price * total_percent)

    ##############################################################

    actual_price = self.order.actual_price
    main_price = self.order.real_order_price

    percent = round(actual_price / (main_price/100))


    booster_price = custom_price * (percent/100)

    percent_for_view = round((booster_price/actual_price)* 100)
    if percent_for_view > 100:
      percent_for_view = 100

    if booster_price > actual_price:
      booster_price = actual_price


    return {"booster_price":booster_price, 'percent_for_view':percent_for_view, 'main_price': main_price-custom_price, 'percent':percent}
  

class HearthStoneBattleOrder(models.Model):
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE)
  current_rank = models.ForeignKey(HearthstoneBattle, on_delete=models.CASCADE, default=None, related_name='current_rank',blank=True, null=True)
  reached_rank = models.ForeignKey(HearthstoneBattle, on_delete=models.CASCADE, default=None, related_name='reached_rank',blank=True, null=True)
  desired_rank = models.ForeignKey(HearthstoneBattle, on_delete=models.CASCADE, default=None, related_name='desired_rank',blank=True, null=True)
  current_division = models.PositiveSmallIntegerField(blank=True, null=True)
  reached_division = models.PositiveSmallIntegerField(blank=True, null=True)
  desired_division = models.PositiveSmallIntegerField(blank=True, null=True)
  current_marks = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
  reached_marks = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
  created_at = models.DateTimeField(auto_now_add =True)
  updated_at = models.DateTimeField(auto_now =True)


  def send_discord_notification(self):
    if self.order.status == 'Extend':
        return print('Extend Order')
    discord_webhook_url = 'https://discordapp.com/api/webhooks/1209758608599031858/PtdjMTcZq9dR5lo9uTVX-cJPSPEduMXcUjoiQrMchDHvyHv0oTuZnCIVIcsX6dwqGCy3'
    current_time = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    embed = {
        "title": "Hearth Stone",
        "description": (
            f"**Order ID:** {self.order.name}\n"
            f" From {str(self.current_rank).upper()} {romanize_division(self.current_division)} Marks {self.current_marks} "
            f" To {str(self.desired_rank).upper()} {romanize_division(self.desired_division)}\n server {self.order.customer_server}"
        ),
        "color": 0x3498db,  # Hex color code for a Discord blue color
        "footer": {"text": f"{current_time}"}, 
    }
    data = {
        "content": "New order has arrived \n",  # Set content to a space if you only want to send an embed
        "embeds": [embed],
    }


    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(discord_webhook_url, json=data, headers=headers)

    if response.status_code != 204:
        print(f"Failed to send Discord notification. Status code: {response.status_code}")


  def save_with_processing(self, *args, **kwargs):
    self.order.game_id = 7
    self.order.game_type = 'A'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'HS{self.order.id}'
    self.order.update_actual_price()
    self.order.save()
    super().save(*args, **kwargs)
    self.send_discord_notification()
    
  def get_details(self):
    return f"From {self.current_division} MMR to {self.desired_division} MMR"

  def __str__(self):
    return self.get_details()
  
  def get_rank_value(self, *args, **kwargs):
    promo_code = f'{None},{None}'

    if self.order.promo_code != None:
      promo_code = f'{self.order.promo_code.code},{self.order.promo_code.discount_amount}'

    return f"{self.current_rank.pk},{self.current_division},{self.current_marks},{self.desired_rank.pk},{self.desired_division},{self.order.duo_boosting},{self.order.select_booster},{self.order.turbo_boost},{self.order.streaming},{0},{self.order.customer_server},{promo_code},2"


  def get_order_price(self):
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

    total_percent = 0

    if self.order.duo_boosting:
      total_percent += 0.65


    if self.order.select_booster:
      total_percent += 0.10


    if self.order.turbo_boost:
      total_percent += 0.20

    
    if self.order.streaming:
      total_percent += 0.15


      
    try:
      promo_code_amount = self.order.promo_code.discount_amount
    except:
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
    curent_mmr_in_c_range, current_range = get_range_current(self.current_division)
    desired_mmr_in_d_range, derired_range = get_range_desired(self.reached_division)
    sliced_prices = full_price_val[current_range : derired_range-1]
    sum_current = curent_mmr_in_c_range * battle_price[current_range-1]
    sum_desired = desired_mmr_in_d_range * battle_price[derired_range-1]
    clear_res = sum(sliced_prices)

    if current_range == derired_range:
        range_value = math.floor((self.reached_division - self.current_division ) / 25)
        price = round(range_value * battle_price[current_range-1], 2)
    else:
        price = round(sum_current + sum_desired + clear_res,2)

    price += (price * total_percent)
    price -= price * (promo_code_amount/100)
    price = round(price, 2)
    custom_price= price
    
    ##############################################################

    actual_price = self.order.actual_price
    main_price = self.order.real_order_price

    percent = round(actual_price / (main_price/100))

    booster_price = custom_price * (percent/100)

    percent_for_view = round((booster_price/actual_price)* 100)
    if percent_for_view > 100:
      percent_for_view = 100

    if booster_price > actual_price:
      booster_price = actual_price


    return {"booster_price":booster_price, 'percent_for_view':percent_for_view, 'main_price': main_price-custom_price, 'percent':percent}





