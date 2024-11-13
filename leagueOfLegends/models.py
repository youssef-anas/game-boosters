from django.db import models
from accounts.models import BaseOrder, Wallet
from accounts.templatetags.custom_filters import romanize_division
import requests
import json
from customer.models import Champion

# Create your models here.
class LeagueOfLegendsRank(models.Model):
  rank_name = models.CharField(max_length=25)
  rank_image = models.ImageField(upload_to='lol/images/', blank=True, null=True)

  def __str__(self):
    return self.rank_name
    
  def get_image_url(self):
    return self.rank_image.url
  
class LeagueOfLegendsTier(models.Model):
  rank = models.OneToOneField('LeagueOfLegendsRank', related_name='tier', on_delete=models.CASCADE)
  from_IV_to_III = models.FloatField(default=0)
  from_III_to_II = models.FloatField(default=0)
  from_II_to_I = models.FloatField(default=0)
  from_I_to_IV_next = models.FloatField(default=0)

  def __str__(self):
    return f"Tiers for {self.rank.rank_name}"

class LeagueOfLegendsMark(models.Model):
  rank = models.OneToOneField('LeagueOfLegendsRank', related_name='mark', on_delete=models.CASCADE)
  marks_0_20 = models.FloatField(default=0)
  marks_21_40 = models.FloatField(default=0)
  marks_41_60 = models.FloatField(default=0)
  marks_61_80 = models.FloatField(default=0)
  marks_81_99 = models.FloatField(default=0)
  marks_series = models.FloatField(default=0)

  def __str__(self):
    return f"Marks For {self.rank}"
  
class LeagueOfLegendsPlacement(models.Model):
  rank_name = models.CharField(max_length=25)
  rank_image = models.ImageField(upload_to='lol/images/', blank=True, null=True)
  price = models.FloatField()

  def __str__(self):
    return self.rank_name
  
  def get_image_url(self):
    if self.rank_image:
      return self.rank_image.url


def get_lol_divisions_data():
    divisions = LeagueOfLegendsTier.objects.all().order_by('id')
    divisions_data = [
        [division.from_IV_to_III, division.from_III_to_II, division.from_II_to_I, division.from_I_to_IV_next]
        for division in divisions
    ]
    return divisions_data

def get_lol_marks_data():
    marks = LeagueOfLegendsMark.objects.all().order_by('id')
    marks_data = [
        [mark.marks_0_20, mark.marks_21_40, mark.marks_41_60, mark.marks_61_80, mark.marks_81_99, mark.marks_series]
        for mark in marks
    ]
    return marks_data

def get_lol_placements_data():
    placements = LeagueOfLegendsPlacement.objects.all().order_by('id')
    placements_data = [placement.price for placement in placements]
    return placements_data



class LeagueOfLegendsDivisionOrder(models.Model):
  DIVISION_CHOICES = [
    (1, 'IV'),
    (2, 'III'),
    (3, 'II'),
    (4, 'I'),
  ]
  MARKS_CHOISES = [
    (0, '0-20'),
    (1 , '21-40'),
    (2, '41-60'),
    (3, '61-80'),
    (4, '81-99'),
    (5, 'series')
  ]
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='lol_division_order')
  current_rank = models.ForeignKey(LeagueOfLegendsRank, on_delete=models.CASCADE, default=None, related_name='current_rank',blank=True, null=True)
  reached_rank = models.ForeignKey(LeagueOfLegendsRank, on_delete=models.CASCADE, default=None, related_name='reached_rank',blank=True, null=True)
  desired_rank = models.ForeignKey(LeagueOfLegendsRank, on_delete=models.CASCADE, default=None, related_name='desired_rank',blank=True, null=True)
  current_division = models.PositiveSmallIntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  reached_division = models.PositiveSmallIntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  desired_division = models.PositiveSmallIntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  current_marks = models.PositiveSmallIntegerField(choices=MARKS_CHOISES,blank=True, null=True)
  reached_marks = models.PositiveSmallIntegerField(choices=MARKS_CHOISES,blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add =True)
  updated_at = models.DateTimeField(auto_now=True)

  select_champion = models.BooleanField(default=True, blank=True, null=True)
  champions = models.ManyToManyField(Champion, related_name='lol_division_champions', blank=True)

  def send_discord_notification(self):
    if self.order.status == 'Extend':
        return print('Extend Order')
    discord_webhook_url = 'https://discordapp.com/api/webhooks/1209755185749168158/GQ9_GQrC5F8ktpEyMK0Qx_tszdrdpYCpVLzm1aY5D3SzFDzudxxQJHPTnaeq5LUnbRxf'
    current_time = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    embed = {
        "title": "LOL",
        "description": (
            f"**Order ID:**  {self.order.name}\n"
            f"From {str(self.current_rank).upper()} {romanize_division(self.current_division)} Marks {self.current_marks} "
            f"To {str(self.desired_rank).upper()} {romanize_division(self.desired_division)} \n"
            f"**server:**  North East \n" # change server next
        ),
        "color": 0x800080,  # Hex color code for a Discord blue color
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
    self.order.game_id = 4
    self.order.game_type = 'D'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'LOL{self.order.id}'
    self.order.update_actual_price()
    self.order.save()
    super().save(*args, **kwargs)
    self.send_discord_notification()
    
  def get_details(self):
    return f"From {str(self.current_rank).upper()} {romanize_division(self.current_division)} {'0-20' if self.current_marks == 0 else ('21-40' if self.current_marks == 1 else ('41-60' if self.current_marks == 2 else ('61-80' if self.current_marks == 3 else ('81-99' if self.current_marks == 4 else 'SERIES'))))} LP To {str(self.desired_rank).upper()} {romanize_division(self.desired_division)}"
  
  def __str__(self):
    return self.get_details()
  
  def get_rank_value(self, *args, **kwargs):
    promo_code = f'{None},{None}'

    if self.order.promo_code != None:
      promo_code = f'{self.order.promo_code.code},{self.order.promo_code.discount_amount}'

    return f"{self.current_rank.pk},{self.current_division},{self.current_marks},{self.desired_rank.pk},{self.desired_division},{self.order.duo_boosting},{self.order.select_booster},{self.order.turbo_boost},{self.order.streaming},{self.select_champion},{self.order.customer_server},{promo_code}"
  
  def get_order_price(self):
    # Read data from utils file
    division_price = get_lol_divisions_data()
    flattened_data = [item for sublist in division_price for item in sublist]
    flattened_data.insert(0,0)
    ##
    marks_data = get_lol_marks_data()
    marks_data.insert(0,[0,0,0,0,0,0])
    ##  
          
    try:
      promo_code_amount = self.order.promo_code.discount_amount
    except:
      promo_code_amount = 0

    current_rank = self.current_rank.pk
    reached_rank = self.reached_rank.pk

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

    start_division = ((current_rank-1)*4) + current_division
    end_division = ((reached_rank-1)*4)+ reached_division
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

class LeagueOfLegendsPlacementOrder(models.Model):
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='lol_placement_order')
  last_rank = models.ForeignKey(LeagueOfLegendsPlacement, on_delete=models.CASCADE, default=None, related_name='last_rank')
  number_of_match = models.IntegerField(default=5)
 
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  select_champion = models.BooleanField(default=False, blank=True, null=True)
  champions = models.ManyToManyField(Champion, related_name='lol_placement_champions', blank=True)


  def send_discord_notification(self):
    if self.order.status == 'Extend':
        return print('Extend Order')
    discord_webhook_url ='https://discordapp.com/api/webhooks/1209755185749168158/GQ9_GQrC5F8ktpEyMK0Qx_tszdrdpYCpVLzm1aY5D3SzFDzudxxQJHPTnaeq5LUnbRxf'
    current_time = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    embed = {
        "title": "LOL",
        "description": (
            f"**Order ID:** {self.order.name}\n"
            f"Placement {self.number_of_match} matchs with last_rank {self.last_rank}"
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
    self.order.game_id = 4
    self.order.game_type = 'P'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'LOL{self.order.id}'
    self.order.update_actual_price()
    self.order.save()
    super().save(*args, **kwargs)
    self.send_discord_notification()

  def get_details(self):
    return f"Boosting of {self.number_of_match} Placement Games With Rank {self.last_rank}"

  def __str__(self):
    return self.get_details()
  
  def get_order_price(self):
    custom_price = self.order.money_owed

    actual_price = self.order.actual_price
    main_price = self.order.real_order_price

    percent = round(actual_price / (main_price/100))

    booster_price = self.order.money_owed

    percent_for_view = round((booster_price/actual_price)* 100)

    return {"booster_price": booster_price, 'percent_for_view':percent_for_view, 'main_price': main_price-custom_price, 'percent':percent}