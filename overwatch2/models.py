from django.db import models
from accounts.models import BaseOrder
from accounts.templatetags.custom_filters import romanize_division
import requests
import json

def get_choices_string(number, CHOICES):
    for value, string in CHOICES:
        if value == number:
            return string
    return None 


class Overwatch2Rank(models.Model):
    rank_name = models.CharField(max_length=25)
    rank_image = models.ImageField(upload_to='overwatch2/images/', blank=True, null=True)

    def __str__(self):
        return self.rank_name
    
    def get_image_url(self):
        return self.rank_image.url

class Overwatch2Tier(models.Model):
    rank = models.OneToOneField(Overwatch2Rank, related_name='tier', on_delete=models.CASCADE)
    from_V_to_IV = models.FloatField(default=0)
    from_IV_to_III = models.FloatField(default=0)
    from_III_to_II = models.FloatField(default=0)
    from_II_to_I = models.FloatField(default=0)
    from_I_to_V_next = models.FloatField(default=0)

    def __str__(self):
        return f"Tiers for {self.rank.rank_name}"

class Overwatch2Mark(models.Model):
    rank = models.OneToOneField(Overwatch2Rank, related_name='mark', on_delete=models.CASCADE)
    mark_number = models.PositiveSmallIntegerField(default=5)
    mark_1 = models.FloatField(default=0)
    mark_2 = models.FloatField(default=0)
    mark_3 = models.FloatField(default=0)
    mark_4 = models.FloatField(default=0)
    mark_5 = models.FloatField(default=0)

    def __str__(self):
        return f"Mark for Rank: {self.rank.rank_name}"
    

def get_overwatch2_divisions_data():
    divisions = Overwatch2Tier.objects.all().order_by('id')
    divisions_data = [
        [division.from_V_to_IV, division.from_IV_to_III, division.from_III_to_II, division.from_II_to_I, division.from_I_to_V_next]
        for division in divisions
    ]
    return divisions_data

def get_overwatch2_marks_data():
    marks = Overwatch2Mark.objects.all().order_by('id')
    marks_data = [
        [mark.mark_1, mark.mark_2, mark.mark_3, mark.mark_4, mark.mark_5]
        for mark in marks
    ]
    return marks_data

def get_overwatch2_placements_data():
    placements = Overwatch2Placement.objects.all().order_by('id')
    placements_data = [
        placement.price
        for placement in placements
    ]
    return placements_data


class Overwatch2DivisionOrder(models.Model):
    DIVISION_CHOICES = [
        (1, 'V'),
        (2, 'IV'),
        (3, 'III'),
        (4, 'II'),
        (5, 'I'),
    ]
    MARKS_CHOISES = [
        (1 , '0-19 %'),
        (2 , '20-39 %'),
        (3 , '40-59 %'),
        (4 , '60-79 %'),
        (5 , '80-99 %'),
    ]
    ROLE_CHOISES = [
        (1 , 'DPS'),
        (2 , 'TANK'),
        (3 , 'SUPPORT'),
    ]
    order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='overwatch2_order')
    current_rank = models.ForeignKey(Overwatch2Rank, on_delete=models.PROTECT, default=None, related_name='current_rank',blank=True, null=False)
    reached_rank = models.ForeignKey(Overwatch2Rank, on_delete=models.PROTECT, default=None, related_name='reached_rank',blank=True, null=True)
    desired_rank = models.ForeignKey(Overwatch2Rank, on_delete=models.PROTECT, default=None, related_name='desired_rank',blank=True, null=False)
    current_division = models.PositiveSmallIntegerField(choices=DIVISION_CHOICES,blank=True, null=False)
    reached_division = models.PositiveSmallIntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
    desired_division = models.PositiveSmallIntegerField(choices=DIVISION_CHOICES,blank=True, null=False)
    current_marks = models.PositiveSmallIntegerField(choices=MARKS_CHOISES,blank=True, null=False)
    reached_marks = models.PositiveSmallIntegerField(choices=MARKS_CHOISES,blank=True, null=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOISES, null=False, blank=True, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # booster_champions = models.BooleanField(default=False, blank=True)


    def send_discord_notification(self):
        if self.order.status == 'Extend':
            return print('Extend Order')
        discord_webhook_url = 'https://discord.com/api/webhooks/1214543233200300083/R2-QI79E4K7UHxpOjbCGbGEytIl7PSmme9qY8flwBIvNraihcRLpTx3vB3qmCYVISLF4'
        current_time = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        embed = {
            "title": "Overwatch 2",
            "description": (
                f"**Order ID:** {self.order.name}\n"
                f" From {str(self.current_rank).upper()} {get_choices_string(self.current_division, self.DIVISION_CHOICES)} Marks {get_choices_string(self.current_marks, self.MARKS_CHOISES)} "
                f" To {str(self.desired_rank).upper()} {get_choices_string(self.desired_division, self.DIVISION_CHOICES)} server {self.order.customer_server}"
            ),
            "color": 0xC0C0C0,  
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
        self.order.game_type = 'D'
        self.order.details = self.get_details()
        # 
        if not self.order.name:
            self.order.name = f'OVW2{self.order.id}'
        self.order.update_actual_price()
        self.order.save()
        super().save(*args, **kwargs)
        self.send_discord_notification()
    
    def get_details(self):
        return f"From {str(self.current_rank).upper()} {get_choices_string(self.current_division, self.DIVISION_CHOICES)} Progress {get_choices_string(self.current_marks, self.MARKS_CHOISES)} To {str(self.desired_rank).upper()} {get_choices_string(self.desired_division, self.DIVISION_CHOICES)}"

    def __str__(self):
        return self.get_details()
    
    
    def get_rank_value(self, *args, **kwargs):
        promo_code = f'{None},{None}'

        if self.order.promo_code != None:
            promo_code = f'{self.order.promo_code.code},{self.order.promo_code.discount_amount}'

        return f"{self.current_rank.pk},{self.current_division},{self.current_marks},{self.desired_rank.pk},{self.desired_division},{self.order.duo_boosting},{self.order.select_booster},{self.order.turbo_boost},{self.order.streaming},{0},{self.order.customer_server},{promo_code}"
    
    def get_order_price(self):
        # Fetch divisions_data using utility function
        divisions_data = get_overwatch2_divisions_data()
        flattened_data = [item for sublist in divisions_data for item in sublist]
        flattened_data.insert(0, 0)
        ##
        marks_data = get_overwatch2_marks_data()
        marks_data.insert(0, [0, 0, 0, 0, 0, 0, 0])
        ##   
        try:    
            promo_code_amount = self.order.promo_code.discount_amount
        except:
            promo_code_amount = 0

        current_rank = self.current_rank.id
        reached_rank = self.reached_rank.id

        current_division = self.current_division
        reached_division = self.reached_division

        current_marks = self.current_marks-1
        reached_marks = self.reached_marks-1

        total_percent = 0

        if self.order.duo_boosting:
            total_percent += 0.65

        if self.order.select_booster:
            total_percent += 0.10

        if self.order.turbo_boost:
            total_percent += 0.20

        if self.order.streaming:
            total_percent += 0.15

        if self.role in [1, 2]:
            role = 0
        elif self.role == 3:
            role = .12
            total_percent += role
        else:
            role = 0


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

class Overwatch2Placement(models.Model):
  rank_name = models.CharField(max_length=25)
  rank_image = models.ImageField(upload_to='overwatch2/images/', blank=True, null=True)
  price = models.FloatField()

  def __str__(self):
    return self.rank_name
  
  def get_image_url(self):
    return self.rank_image.url

class Overwatch2PlacementOrder(models.Model):
  ROLE_CHOISES = [
        (1 , 'DPS'),
        (2 , 'TANK'),
        (3 , 'SUPPORT'),
  ]
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='ovw2_placement_order')
  last_rank = models.ForeignKey(Overwatch2Placement, on_delete=models.CASCADE, default=None, related_name='ovw2_last_rank')
  number_of_match = models.IntegerField(default=5)
  role = models.PositiveSmallIntegerField(choices=ROLE_CHOISES, null=False, blank=True, default=0)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  select_champions = models.BooleanField(default=False, blank=True, null=True)

  def send_discord_notification(self):
    if self.order.status == 'Extend':
        return print('Extend Order')
    discord_webhook_url ='https://discord.com/api/webhooks/1214543233200300083/R2-QI79E4K7UHxpOjbCGbGEytIl7PSmme9qY8flwBIvNraihcRLpTx3vB3qmCYVISLF4'
    current_time = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    embed = {
        "title": "OverWatch 2",
        "description": (
            f"**Order ID:** {self.order.name}\n"
            f"Placement {self.number_of_match} matchs with last rank {self.last_rank}"
        ),
        "color": 0xC0C0C0, 
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
    self.order.game_type = 'P'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'OVW2{self.order.id}'
    self.order.update_actual_price()
    self.order.save()
    super().save(*args, **kwargs)
    self.send_discord_notification()

  def get_details(self):
    return f"Boosting of {self.number_of_match} Placement Games With Last Rank {self.last_rank}"

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