from django.db import models
from accounts.models import BaseOrder, Wallet
from accounts.templatetags.custom_filters import ten_romanize_division,romanize_division
import requests
import json

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

    return f"{self.current_rank.pk},{self.current_division},{self.current_marks},{self.desired_rank.pk},{self.desired_division},{self.order.duo_boosting},{self.order.select_booster},{self.order.turbo_boost},{self.order.streaming},{0},{self.order.customer_server},{promo_code}"

  def get_order_price(self):
    # Read data from JSON file
    with open('static/hearthstone/data/divisions_data.json', 'r') as file:
      division_price = json.load(file)
      flattened_data = [item for sublist in division_price for item in sublist]
      flattened_data.insert(0,0)
    ##
    with open('static/hearthstone/data/marks_data.json', 'r') as file:
      marks_data = json.load(file)
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

    start_division = ((current_rank-1) * 10) + current_division
    end_division = ((reached_rank-1) * 10)+ reached_division
    marks_price = marks_data[current_rank][current_marks]
    marks_price_reached = 0
    marks_price_reached = marks_data[reached_rank][reached_marks]

    sublist = flattened_data[start_division:end_division]


    total_sum = sum(sublist)    


    custom_price = total_sum - marks_price + marks_price_reached
    
    custom_price += (custom_price * total_percent)
    custom_price -= custom_price * (promo_code_amount/100)

    ##############################################################

    actual_price = self.order.actual_price
    main_price = self.order.price

    percent = round(actual_price / (main_price/100))

    print(percent)

    booster_price = custom_price * (percent/100)

    percent_for_view = round((booster_price/actual_price)* 100)
    if percent_for_view > 100:
      percent_for_view = 100

    if booster_price > actual_price:
      booster_price = actual_price


    return {"booster_price":booster_price, 'percent_for_view':percent_for_view, 'main_price': main_price-custom_price, 'percent':percent}