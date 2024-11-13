from django.db import models
from accounts.models import BaseOrder, Wallet
from accounts.templatetags.custom_filters import five_romanize_division
import json
import requests

# Create your models here.
class HonorOfKingsRank(models.Model):
  rank_name = models.CharField(max_length=25)
  rank_image = models.ImageField(upload_to='hok/images/', blank=True, null=True)

  def __str__(self):
    return self.rank_name
    
  def get_image_url(self):
    return self.rank_image.url
  
class HonorOfKingsTier(models.Model):
  rank = models.OneToOneField('HonorOfKingsRank', related_name='tier', on_delete=models.CASCADE)
  from_V_to_IV = models.FloatField(default=0)
  from_IV_to_III = models.FloatField(default=0)
  from_III_to_II = models.FloatField(default=0)
  from_II_to_I = models.FloatField(default=0)
  from_I_to_IV_next = models.FloatField(default=0)

  def __str__(self):
    return f"Tiers for {self.rank.rank_name}"

class HonorOfKingsMark(models.Model):
  rank = models.OneToOneField('HonorOfKingsRank', related_name='mark', on_delete=models.CASCADE)
  star_1 = models.FloatField(default=0)
  star_2 = models.FloatField(default=0)
  star_3 = models.FloatField(default=0)

  def __str__(self):
    return f"{self.rank} -> Star 1: {self.star_1}, Star 2: {self.star_2}, Star 3: {self.star_3}"

def get_hok_divisions_data():
    divisions = HonorOfKingsTier.objects.all().order_by('id')
    divisions_data = [
        [division.from_V_to_IV, division.from_IV_to_III, division.from_III_to_II, division.from_II_to_I, division.from_I_to_IV_next]
        for division in divisions
    ]
    return divisions_data

def get_hok_marks_data():
    marks = HonorOfKingsMark.objects.all().order_by('id')
    marks_data = [
        [0, mark.star_1, mark.star_2, mark.star_3]
        for mark in marks
    ]
    return marks_data


class HonorOfKingsDivisionOrder(models.Model):
  DIVISION_CHOICES = [
    (1, 'V'),
    (2, 'IV'),
    (3, 'III'),
    (4, 'II'),
    (5, 'I'),
  ]
  MARKS_CHOISES = [
    (0, '0 Stars'),
    (1, '1 Stars'),
    (2, '2 Stars'),
    (3, '3 Stars'),
  ]
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='hok_division_order')
  current_rank = models.ForeignKey(HonorOfKingsRank, on_delete=models.CASCADE, default=None, related_name='current_rank',blank=True, null=True)
  reached_rank = models.ForeignKey(HonorOfKingsRank, on_delete=models.CASCADE, default=None, related_name='reached_rank',blank=True, null=True)
  desired_rank = models.ForeignKey(HonorOfKingsRank, on_delete=models.CASCADE, default=None, related_name='desired_rank',blank=True, null=True)
  current_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  reached_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  desired_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  current_marks = models.IntegerField(choices=MARKS_CHOISES,blank=True, null=True)
  reached_marks = models.IntegerField(choices=MARKS_CHOISES,blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add =True)
  updated_at = models.DateTimeField(auto_now =True)


  def send_discord_notification(self):
    if self.order.status == 'Extend':
        return print('Extend Order')
    discord_webhook_url = 'https://discord.com/api/webhooks/1218995123841663006/VCxXOoREssz7jgyXnKmxRVB6qINi15FccHPMt0gCJALNNf1LBzaZsgyV8cXL5lZEy6sw'
    current_time = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    embed = {
        "title": "Honor Of Kings",
        "description": (
            f"**Order ID:** {self.order.name}\n"
            f"From {str(self.current_rank).upper()} {five_romanize_division(self.current_division)} Marks {self.current_marks} "
            f"To {str(self.desired_rank).upper()} {five_romanize_division(self.desired_division)} \nserver {self.order.customer_server}"
        ),
        "color": 0x3498db,
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
    # self.order.game_id = 11
    # self.order.game_type = 'D'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'HOK{self.order.id}'
    self.order.update_actual_price()
    self.order.save()
    super().save(*args, **kwargs)
    self.send_discord_notification()
    
  def get_details(self):
    return f"From {str(self.current_rank).upper()} {five_romanize_division(self.current_division)} {self.current_marks} Stars To {str(self.desired_rank).upper()} {five_romanize_division(self.desired_division)}"

  def __str__(self):
    return self.get_details()
  
  def get_rank_value(self, *args, **kwargs):
    promo_code = f'{None},{None}'

    if self.order.promo_code != None:
      promo_code = f'{self.order.promo_code.code},{self.order.promo_code.discount_amount}'

    return f"{self.current_rank.pk},{self.current_division},{self.current_marks},{self.desired_rank.pk},{self.desired_division},{self.order.duo_boosting},{self.order.select_booster},{self.order.turbo_boost},{self.order.streaming},{0},{self.order.customer_server},{promo_code}"
    

  def get_order_price(self):
    # Read data from utils file
    division_price = get_hok_divisions_data()
    flattened_data = [item for sublist in division_price for item in sublist]
    flattened_data.insert(0,0)
    ##
    marks_data = get_hok_marks_data()
    marks_data.insert(0,[0,0,0,0])
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