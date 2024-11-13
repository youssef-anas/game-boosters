from django.db import models
from accounts.models import BaseOrder, Wallet
from accounts.templatetags.custom_filters import romanize_division
from django.core.validators import MinValueValidator, MaxValueValidator
import requests
from django.core.exceptions import ValidationError
from mobileLegends.validators import validate_current_rank_mobile_legends


class MobileLegendsRank(models.Model):
  rank_name = models.CharField(max_length=25)
  rank_image = models.ImageField(upload_to='mobile_legends/images/', blank=True, null=True)

  def __str__(self):
    return self.rank_name
    
  def get_image_url(self):
    return self.rank_image.url
  
class MobileLegendsTier(models.Model):
  rank = models.OneToOneField(MobileLegendsRank, related_name='tier', on_delete=models.CASCADE)
  from_V_to_IV = models.FloatField(default=0)
  from_IV_to_III = models.FloatField(default=0)
  from_III_to_II = models.FloatField(default=0)
  from_II_to_I = models.FloatField(default=0)
  from_I_to_V_next = models.FloatField(default=0)

  def __str__(self):
    return f"Tiers for {self.rank.rank_name}"

class MobileLegendsMark(models.Model):
  rank = models.OneToOneField('MobileLegendsRank', related_name='mark', on_delete=models.CASCADE)
  star_1 = models.FloatField(default=0)
  star_2 = models.FloatField(default=0)
  star_3 = models.FloatField(default=0)
  star_4 = models.FloatField(default=0)
  star_5 = models.FloatField(default=0)

  def __str__(self):
    return f"{self.rank} Marks"
  
class MobileLegendsPlacement(models.Model):
  rank_name = models.CharField(max_length=25)
  rank_image = models.ImageField(upload_to='mobile_legends/images/', blank=True, null=True)
  price = models.FloatField()

  def __str__(self):
    return self.rank_name
  
  def get_image_url(self):
    return self.rank_image.url
  
def get_mobile_legends_divisions_data():
    divisions = MobileLegendsTier.objects.all().order_by('id')
    return [
        [division.from_V_to_IV, division.from_IV_to_III, division.from_III_to_II, division.from_II_to_I, division.from_I_to_V_next]
        for division in divisions
    ]

def get_mobile_legends_marks_data():
    marks = MobileLegendsMark.objects.all().order_by('id')
    return [
        [mark.star_1, mark.star_2, mark.star_3, mark.star_4, mark.star_5]
        for mark in marks
    ]

def get_mobile_legends_placements_data():
    placements = MobileLegendsPlacement.objects.all().order_by('id')
    return [
        placement.price
        for placement in placements
    ]


class MobileLegendsDivisionOrder(models.Model):
  @staticmethod
  def generate_choices(rank_id):
      if rank_id == 7:
          return [
              (1, '0-4 Stars'),
              (2, '5-9 Stars'),
              (3, '10-14 Stars'),
              (4, '15-19 Stars'),
              (5, '20-24 Stars'),
          ]
      elif rank_id == 8:
          return [
              (1, '25-29 Stars'),
              (2, '30-34 Stars'),
              (3, '35-39 Stars'),
              (4, '40-44 Stars'),
              (5, '44-49 Stars'),
          ]
      elif rank_id == 9:
          return [
              (1, '50-59 Stars'),
              (2, '60-69 Stars'),
              (3, '70-79 Stars'),
              (4, '80-89 Stars'),
              (5, '90-99 Stars'),
          ]
      elif rank_id == 10:
          return [
              (1, '-'),
              (2, '-'),
              (3, '-'),
              (4, '-'),
              (5, '-'),
          ]
      else:
          # default choices
          return [
              (1, 'V'),
              (2, 'IV'),
              (3, 'III'),
              (4, 'II'),
              (5, 'I'),
          ]

  MARKS_CHOICES = [
      (0, '0 Star'),
      (1, '1 Star'),
      (2, '2 Star'),
      (3, '3 Star'),
      (4, '4 Star'),
      (5, '5 Star'),
  ]

  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='mobile_legends_division_order')
  current_rank = models.ForeignKey(MobileLegendsRank, on_delete=models.CASCADE, default=None, related_name='current_rank', blank=True, null=True, limit_choices_to={'id__range': (1, 9)})
  reached_rank = models.ForeignKey(MobileLegendsRank, on_delete=models.CASCADE, default=None, related_name='reached_rank', blank=True, null=True, limit_choices_to={'id__range': (1, 10)})
  desired_rank = models.ForeignKey(MobileLegendsRank, on_delete=models.CASCADE, default=None, related_name='desired_rank', blank=True, null=True, limit_choices_to={'id__range': (1, 10)})

  current_division = models.PositiveSmallIntegerField(choices=[], blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
  reached_division = models.PositiveSmallIntegerField(choices=[], blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
  desired_division = models.PositiveSmallIntegerField(choices=[], blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])

  current_marks = models.PositiveSmallIntegerField(choices=MARKS_CHOICES, blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
  reached_marks = models.PositiveSmallIntegerField(choices=MARKS_CHOICES, blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  select_champion = models.BooleanField(default=True, blank=True, null=True)


  def save(self, *args, **kwargs):
      super().save(*args, **kwargs)

  def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      if self.current_rank:
          self._meta.get_field('current_division').choices = self.generate_choices(self.current_rank.id)
      if self.reached_rank:
          self._meta.get_field('reached_division').choices = self.generate_choices(self.reached_rank.id)
      if self.desired_rank:
          self._meta.get_field('desired_division').choices = self.generate_choices(self.desired_rank.id)

  def clean(self):
        validate_current_rank_mobile_legends(self.current_rank.id, self.current_division, self.current_marks)
        validate_current_rank_mobile_legends(self.reached_rank.id, self.reached_division, self.reached_marks)
        validate_current_rank_mobile_legends(self.desired_rank.id, self.desired_division, 1)

  def send_discord_notification(self):
    if self.order.status == 'Extend':
        return print('Extend Order')
    discord_webhook_url = 'https://discordapp.com/api/webhooks/1209760345074171955/r_wFIUaPEIQevGJ1WYj0oVyHNNm_5mtM5g5mB-Ctzq8_npLbfGMrNhFA-2W_CwUXhTj1'
    current_time = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    embed = {
        "title": "Mobile Legends",
        "description": (
            f"**Order ID:** {self.order.name}\n"
            f"From {str(self.current_rank).upper()} {romanize_division(self.current_division)} Marks {self.current_marks} "
            f"To {str(self.desired_rank).upper()} {romanize_division(self.desired_division)} \n server {self.order.customer_server}"
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
    self.order.game_id = 8
    self.order.game_type = 'D'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'MOBLEG{self.order.id}'
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
    
    division_price = get_mobile_legends_divisions_data()
    flattened_data = [item for sublist in division_price for item in sublist]
    flattened_data.insert(0, 0)
    ##
    marks_data = get_mobile_legends_marks_data()
    marks_data.insert(0,[0,0,0,0,0,0])
    pass
    ## 
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

    current_rank = self.current_rank.pk
    reached_rank = self.reached_rank.pk

    current_division = self.current_division
    reached_division = self.reached_division

    current_marks = self.current_marks
    reached_marks = self.reached_marks
    
    start_division = ((current_rank-1) * 5) + current_division
    end_division = ((reached_rank-1) * 5)+ reached_division

    marks_price = marks_data[current_rank][current_marks]
    marks_price_reached = marks_data[current_rank][reached_marks]

    sublist = flattened_data[start_division:end_division ]
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
  
class MobileLegendsPlacementOrder(models.Model):
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='mob_leg_placement_order')
  last_rank = models.ForeignKey(MobileLegendsPlacement, on_delete=models.CASCADE, default=None, related_name='mob_leg_last_rank')
  number_of_match = models.IntegerField(default=5)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  select_champion = models.BooleanField(default=False, blank=True, null=True)

  def send_discord_notification(self):
    if self.order.status == 'Extend':
        return print('Extend Order')
    discord_webhook_url ='https://discordapp.com/api/webhooks/1209760345074171955/r_wFIUaPEIQevGJ1WYj0oVyHNNm_5mtM5g5mB-Ctzq8_npLbfGMrNhFA-2W_CwUXhTj1'
    current_time = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    embed = {
        "title": "Mobile Legends",
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
    # self.order.game_id = 8
    # self.order.game_name = 'mobileLegends'
    self.order.game_type = 'P'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'MOBLEG{self.order.id}'
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