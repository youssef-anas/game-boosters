from django.db import models
from accounts.models import BaseOrder
import requests
from django.core.exceptions import ValidationError
import json
import math

class Dota2Rank(models.Model):
  rank_name = models.CharField(max_length=25)
  rank_image = models.ImageField(upload_to='dota2/images/', blank=True, null=True)
  start_RP = models.IntegerField()
  end_RP = models.IntegerField()

  def __str__(self):
    return self.rank_name
    
  def get_image_url(self):
    return self.rank_image.url
  
class SingletonModel(models.Model):
  class Meta:
    abstract = True

  @classmethod
  def load(cls):
    obj, created = cls.objects.get_or_create(pk=1)
    return obj

  def save(self, *args, **kwargs):
    self.pk = 1
    super().save(*args, **kwargs)

  def delete(self, *args, **kwargs):
    pass

class Dota2MmrPrice(SingletonModel):
  price_0_2000 = models.FloatField(default=1)
  price_2000_3000 = models.FloatField(default=1)
  price_3000_4000 = models.FloatField(default=1)
  price_4000_5000 = models.FloatField(default=1)
  price_5000_5500 = models.FloatField(default=1)
  price_5500_6000 = models.FloatField(default=1)
  price_6000_extra = models.FloatField(default=1)

  def __str__(self):
    return f"Price for 50 RPs is {self.price_0_2000}, {self.price_2000_3000}, {self.price_3000_4000}, {self.price_4000_5000}, {self.price_5000_5500}, {self.price_5500_6000}, {self.price_6000_extra}"
  
  def save(self, *args, **kwargs):
    self.pk = 1
    super().save(*args, **kwargs)
  
class Dota2Placement(models.Model):
  rank_name = models.CharField(max_length=25)
  rank_image = models.ImageField(upload_to='dota2/images/', blank=True, null=True)
  start_RP = models.IntegerField()
  end_RP = models.IntegerField()
  price = models.FloatField()

  def __str__(self):
    return self.rank_name
  
  def get_image_url(self):
    return self.rank_image.url
  


def get_division_prices():
  division_row = Dota2MmrPrice.objects.all().first()
  division_prices = [
      division_row.price_0_2000,
      division_row.price_2000_3000,
      division_row.price_3000_4000,
      division_row.price_4000_5000,
      division_row.price_5000_5500,
      division_row.price_5500_6000,
      division_row.price_6000_extra
  ]
  return division_prices

def get_placement_prices():
  placement_rows = Dota2Placement.objects.all().order_by('id')
  placement_prices = [row.price for row in placement_rows]
  return placement_prices  



class Dota2RankBoostOrder(models.Model):
  ROLE_CHOISES = (
    (1, 'Core'),
    (2, 'Support'),
  )
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='dota2_division_order')

  current_rank = models.ForeignKey(Dota2Rank, on_delete=models.CASCADE, default=None, related_name='dota2_current_rank')
  reached_rank = models.ForeignKey(Dota2Rank, on_delete=models.CASCADE, default=None, related_name='dota2_reached_rank')
  desired_rank = models.ForeignKey(Dota2Rank, on_delete=models.CASCADE, default=None, related_name='dota2_desired_rank')

  current_division = models.IntegerField(default=0)
  reached_division = models.IntegerField(default=0)
  desired_division = models.IntegerField(default=0)

  current_marks = models.PositiveSmallIntegerField(blank=True, null=True, default= 0)
  reached_marks = models.PositiveSmallIntegerField(blank=True, null=True, default= 0)

  role = models.PositiveSmallIntegerField(choices=ROLE_CHOISES, null=True, blank=True)
  
  created_at = models.DateTimeField(auto_now_add =True)


  def validate_divition(self):
    if not (self.current_division >= 0 and self.current_division <= 7000):
      raise ValidationError("Current division must be between 0 and 7000.")
        
  def send_discord_notification(self):
    if self.order.status == 'Extend':
      return print('Extend Order')
    discord_webhook_url = 'https://discord.com/api/webhooks/1218196265163292734/M5Pl0WbSe_bHWXaRdcpzoSg2tbn5NONzqwGBg2e2kv62AUOfW658U-_SxAO_P_PoX5eB'
    current_time = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    embed = {
      "title": "Dota 2",
      "description": (
        f"**Order ID:** {self.order.name}\n"
        f" From {self.current_division} RP"
        f" To {self.desired_division} RP role {self.get_role_display()} server {self.order.customer_server}"
      ),
      "color": 0xFFA500,  # Hex color code for a Discord color
      "footer": {"text": f"{current_time}"}, 
    }
    data = {
      "content": "New order has arrived \n",
      "embeds": [embed],
    }

    headers = {
      "Content-Type": "application/json"
    }

    response = requests.post(discord_webhook_url, json=data, headers=headers)

    if response.status_code != 204:
      print(f"Failed to send Discord notification. Status code: {response.status_code}")


  def save_with_processing(self, *args, **kwargs):
    self.validate_divition()
    # self.order.game_id = 10
    self.order.game_type = 'A'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'Dot{self.order.id}'
    self.order.update_actual_price()
    self.order.save()
    super().save(*args, **kwargs)
    self.send_discord_notification()

  def get_details(self):
      return f"From {self.current_division} RP To {self.desired_division}"
    
  def __str__(self):
    return f"Boosting From {self.current_division} RP To {self.desired_division}"

  def get_rank_value(self, *args, **kwargs):
    promo_code = f'{None},{None}'

    if self.order.promo_code != None:
      promo_code = f'{self.order.promo_code.code},{self.order.promo_code.discount_amount}'

    return f"{self.current_rank.pk},{self.current_division},{0},{self.desired_rank.pk},{self.desired_division},{self.order.duo_boosting},{self.order.select_booster},{self.order.turbo_boost},{self.order.streaming},{self.select_champion},{self.order.customer_server},{promo_code},{self.role}"
  
  def get_order_price(self):
    divison_prices = get_division_prices()
      
    divison_prices.insert(0,0)
    price1 = round(divison_prices[1]*40,1)
    price2 = round(divison_prices[2]*20,1)
    price3 = round(divison_prices[3]*20,1)
    price4 = round(divison_prices[4]*20,1)
    price5 = round(divison_prices[5]*10,1)
    price6 = round(divison_prices[6]*10,1)
    price7 = round(divison_prices[7]*40,1) 
    full_price_val = [price1, price2, price3, price4, price5, price6, price7]

    def get_range_current(mmr):
      MAX_LISTS = [2000, 3000, 4000, 5000, 5500, 6000, 8000]
      for idx, max_val in enumerate(MAX_LISTS, start=1):
          if mmr <= max_val:
              val = max_val - mmr
              return math.floor(val/50), idx
      print('out_of_range')
      return None, None
        
    def get_range_desired(mmr):
      MAX_LISTS = [2000, 3000, 4000, 5000, 5500, 6000, 8000]
      for idx, max_val in enumerate(MAX_LISTS, start=1):
          if mmr <= max_val:
              val = mmr-MAX_LISTS[idx-2]
              return math.floor(val/50), idx
      print('out_of_range')
      return None, None

    try:    
      promo_code_amount = self.order.promo_code.discount_amount
    except:
      promo_code_amount = 0

    ROLE_PRICES = [0, 0, 0.30]

    current_division = self.current_division
    reached_division = self.reached_division

    role = self.role
    
    total_percent = 0

    if self.order.duo_boosting:
      total_percent += 0.65

    if self.order.select_booster:
      total_percent += 0.10

    if self.order.turbo_boost:
      total_percent += 0.20

    if self.order.streaming:
      total_percent += 0.15

    curent_mmr_in_c_range, current_range = get_range_current(current_division)  
    desired_mmr_in_d_range, derired_range = get_range_desired(reached_division)
    sliced_prices = full_price_val[current_range :derired_range - 1]
    sum_current = curent_mmr_in_c_range * divison_prices[current_range]
    sum_desired = desired_mmr_in_d_range * divison_prices[derired_range]
    clear_res = sum(sliced_prices)
   # full price for all rank [159.2, 92.6, 116.4, 213, 198.6, 244.6, 1520.4]
    if current_range == derired_range:
      if not current_division == 0:
        current_division -= 1
      range_value = math.floor((reached_division - current_division )/50)
      custom_price = round(range_value * divison_prices[current_range], 2)
    else:
      custom_price = round(sum_current + sum_desired + clear_res,2)

    total_Percentage_with_role_result = total_percent + ROLE_PRICES[role]
    
    custom_price += custom_price * total_Percentage_with_role_result

    custom_price -= custom_price * (promo_code_amount / 100)

    actual_price = self.order.actual_price
    main_price = self.order.real_order_price

    percent = round(actual_price / (main_price / 100))
    booster_price = round(custom_price * (percent / 100), 2)
    percent_for_view = round((booster_price / actual_price) * 100)

    if percent_for_view > 100:
        percent_for_view = 100

    if booster_price > actual_price:
        booster_price = actual_price

    return {"booster_price":booster_price, 'percent_for_view':percent_for_view, 'main_price': main_price-custom_price, 'percent':percent}

class Dota2PlacementOrder(models.Model):
  ROLE_CHOISES = (
    (1, 'Core'),
    (2, 'Support'),
  )
   
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='dota2_placement_order')
  last_rank = models.ForeignKey(Dota2Placement, on_delete=models.CASCADE, default=None, related_name='last_rank')
  last_division = models.IntegerField(default=0)
  number_of_match = models.IntegerField(default=0)
  role = models.PositiveSmallIntegerField(choices=ROLE_CHOISES, null=True, blank=True)
  select_champion = models.BooleanField(default=False, blank=True, null=True)

  def save_with_processing(self, *args, **kwargs):
    # self.order.game_id = 10
    self.order.game_type = 'P'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'Dota2{self.order.id}'
    self.order.update_actual_price()
    self.order.save()
    super().save(*args, **kwargs)
    # self.send_discord_notification(self)

  def get_details(self):
    return f"Boosting of {self.number_of_match} Placement Games With Rank {self.last_rank}"

  def __str__(self):
    return self.get_details()
  
  def get_order_price(self):
    placement_price = get_placement_prices()

    try:    
      promo_code_amount = self.order.promo_code.discount_amount
    except:
      promo_code_amount = 0

    ROLE_PRICES = [0, 0, 0.30]

    last_rank = self.last_rank.pk
    number_of_match = self.number_of_match

    role = self.role
    
    total_percent = 0

    if self.order.duo_boosting:
      total_percent += 0.65

    if self.order.select_booster:
      total_percent += 0.10

    if self.order.turbo_boost:
      total_percent += 0.20

    if self.order.streaming:
      total_percent += 0.15

    custom_price = placement_price[last_rank - 1] * number_of_match

    total_Percentage_with_role_result = total_percent + ROLE_PRICES[role]

    custom_price += (custom_price * total_Percentage_with_role_result)


    custom_price = round(custom_price, 2)
    
    actual_price = self.order.actual_price
    main_price = self.order.real_order_price

    percent = round(actual_price / (main_price / 100))

    booster_price = round(custom_price * (percent / 100), 2)
    percent_for_view = round((booster_price / actual_price) * 100)

    if percent_for_view > 100:
        percent_for_view = 100

    if booster_price > actual_price:
        booster_price = actual_price

    return {"booster_price":booster_price, 'percent_for_view':percent_for_view, 'main_price': main_price-custom_price, 'percent':percent}