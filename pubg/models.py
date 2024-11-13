from django.db import models
from accounts.models import BaseOrder
from accounts.templatetags.custom_filters import five_romanize_division, romanize_division_original
import requests

class PubgRank(models.Model):
  rank_name = models.CharField(max_length=25, default='rank name')
  rank_image = models.ImageField(upload_to='pubg/images/', blank=True, null=True)

  def __str__(self):
    return self.rank_name
    
  def get_image_url(self):
    return self.rank_image.url
  
class PubgTier(models.Model):
  rank = models.OneToOneField('PubgRank', related_name='tier', on_delete=models.CASCADE, null=True)
  from_V_to_VI = models.FloatField(default=0)
  from_VI_to_III = models.FloatField(default=0)
  from_III_to_II = models.FloatField(default=0)
  from_II_to_I = models.FloatField(default=0)
  from_I_to_V_next = models.FloatField(default=0)

  def __str__(self):
    return f"Tiers for {self.rank.rank_name}"


class PubgMark(models.Model):
  rank = models.OneToOneField('PubgRank', related_name='mark', on_delete=models.CASCADE, null=True)
  marks_0_20 = models.FloatField(default=0)
  marks_21_40 = models.FloatField(default=0)
  marks_41_60 = models.FloatField(default=0)
  marks_61_80 = models.FloatField(default=0)
  marks_81_100 = models.FloatField(default=0)

  def __str__(self):
    return f"Marks for {self.rank}"
  
def get_divisions_data():
    divisions = PubgTier.objects.all().order_by('id')
    divisions_data = [
        [division.from_V_to_VI, division.from_VI_to_III, division.from_III_to_II, division.from_II_to_I, division.from_I_to_V_next]
        for division in divisions
    ]
    return divisions_data

def get_marks_data():
    marks = PubgMark.objects.all().order_by('id')
    marks_data = [
        [mark.marks_0_20, mark.marks_21_40, mark.marks_41_60, mark.marks_61_80, mark.marks_81_100]
        for mark in marks
    ]
    return marks_data  
  
  
class PubgDivisionOrder(models.Model):
  DIVISION_CHOICES = [
    (1, 'V'),
    (2, 'IV'),
    (3, 'III'),
    (4, 'II'),
    (5, 'I'),
  ]
  MARKS_CHOISES = [
    (0, '0-20'),
    (1 , '21-40'),
    (2, '41-60'),
    (3, '61-80'),
    (4, '81-100')
  ]
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='pubg_division_order')
  current_rank = models.ForeignKey(PubgRank, on_delete=models.CASCADE, default=None, related_name='current_rank',blank=True, null=True)
  reached_rank = models.ForeignKey(PubgRank, on_delete=models.CASCADE, default=None, related_name='reached_rank',blank=True, null=True)
  desired_rank = models.ForeignKey(PubgRank, on_delete=models.CASCADE, default=None, related_name='desired_rank',blank=True, null=True)
  current_division = models.PositiveSmallIntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  reached_division = models.PositiveSmallIntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  desired_division = models.PositiveSmallIntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  current_marks = models.PositiveSmallIntegerField(choices=MARKS_CHOISES,blank=True, null=True)
  reached_marks = models.PositiveSmallIntegerField(choices=MARKS_CHOISES,blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add =True)
  updated_at = models.DateTimeField(auto_now =True)

  select_champion = models.BooleanField(default=True, blank=True, null=True)

  def send_discord_notification(self):
    try:  
      if self.order.status == 'Extend':
        return print('Extend Order')
      discord_webhook_url = 'https://discord.com/api/webhooks/1193142919620743258/fMYJS3jtU3Z2g8gON6UuHj9GKc1NEVRzor-8P9iWIMgNkiZTELCVfJysmXspeVHaSQxt'
      current_time = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
      embed = {
        "title": "Pubg",
        "description": (
          f"**Order ID:** {self.order.name}\n"
          f" From {str(self.current_rank).upper()} {five_romanize_division(self.current_division)} "
          f" To {str(self.desired_rank).upper()} {five_romanize_division(self.desired_division)} server {self.current_marks}"
        ),
        "color": 0x800080,  # Hex color code for a Discord color
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
    except:
       pass


  def save_with_processing(self, *args, **kwargs):
    self.order.game_type = 'D'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'Pubg{self.order.id}'
    self.order.update_actual_price()
    self.order.save()
    super().save(*args, **kwargs)
    self.send_discord_notification()

  def get_details(self):
      return f"From {str(self.current_rank).upper()} {five_romanize_division(self.current_division)} points {self.current_marks} To {str(self.desired_rank).upper()} {five_romanize_division(self.desired_division)}"
  def __str__(self):
    return f"Boosting From {str(self.current_rank).upper()} {five_romanize_division(self.current_division)} points {self.current_marks} To {str(self.desired_rank).upper()} {five_romanize_division(self.desired_division)}"

  def get_rank_value(self, *args, **kwargs):
      promo_code = f'{None},{None}'

      if self.order.promo_code != None:
          promo_code = f'{self.order.promo_code.code},{self.order.promo_code.discount_amount}'

      return f"{self.current_rank.pk},{self.current_division},{self.current_marks},{self.desired_rank.pk},{self.desired_division},{self.order.duo_boosting},{self.order.select_booster},{self.order.turbo_boost},{self.order.streaming},{0},{self.order.customer_server},{promo_code}"
  
  def get_order_price(self):
      # Fetch divisions data using utility function
      divisions_data = get_divisions_data()
      flattened_data = [item for sublist in divisions_data for item in sublist]
      flattened_data.insert(0, 0)

      # Fetch marks data using utility function
      marks_data = get_marks_data()
      marks_data.insert(0, [0, 0, 0, 0, 0, 0])
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


      start_division = ((current_rank-1)*5) + current_division
      end_division = ((reached_rank-1)*5)+ reached_division
      marks_price = marks_data[current_rank][current_marks]

      marks_price_reached = marks_data[reached_rank][reached_marks]

      sublist = flattened_data[start_division:end_division]

      total_sum = sum(sublist)    

      custom_price = total_sum - marks_price + marks_price_reached
      
      custom_price += (custom_price * total_percent)
      ##############################################################

      actual_price = self.order.actual_price
      main_price = self.order.real_order_price

      percent = round(actual_price / (main_price/100))

      booster_price = round(custom_price * (percent/100), 2)
      percent_for_view = round((booster_price/actual_price)* 100)

      if percent_for_view > 100:
          percent_for_view = 100

      if booster_price > actual_price:
          booster_price = actual_price

      return {"booster_price":booster_price, 'percent_for_view':percent_for_view, 'main_price': main_price-custom_price, 'percent':percent}