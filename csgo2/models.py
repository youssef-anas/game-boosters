from django.db import models
from accounts.models import BaseOrder
from accounts.templatetags.custom_filters import romanize_division
import requests
import json


class Csgo2Rank(models.Model):
    rank_name = models.CharField(max_length=25)
    rank_image = models.ImageField(upload_to='csgo2/images/', blank=True, null=True)

    def __str__(self):
        return self.rank_name
    
    def get_image_url(self):
        return f"/media/{self.rank_image}"
    

class Csgo2Tier(models.Model):
    rank = models.OneToOneField(Csgo2Rank, related_name='tier', on_delete=models.CASCADE)
    from_I_to_I_next = models.FloatField(default=0)

    def __str__(self):
        return f"Tiers for {self.rank.rank_name}"
    

class Csgo2Mark(models.Model):
    rank = models.OneToOneField(Csgo2Rank, related_name='mark', on_delete=models.CASCADE)
    mark_number = models.PositiveSmallIntegerField(default=5)

    def __str__(self):
        return f"Mark for Rank: {self.rank.rank_name}"
    
class Csgo2DivisionOrder(models.Model):
    order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='csgo2_order')
    current_rank = models.ForeignKey(Csgo2Rank, on_delete=models.PROTECT, default=None, related_name='current_rank',blank=True, null=False)
    reached_rank = models.ForeignKey(Csgo2Rank, on_delete=models.PROTECT, default=None, related_name='reached_rank',blank=True, null=True)
    desired_rank = models.ForeignKey(Csgo2Rank, on_delete=models.PROTECT, default=None, related_name='desired_rank',blank=True, null=False)
    current_division = models.PositiveSmallIntegerField(blank=True, null=False,default=1)
    reached_division = models.PositiveSmallIntegerField(blank=True, null=True,default=1)
    desired_division = models.PositiveSmallIntegerField(blank=True, null=False,default=1)
    current_marks = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    reached_marks = models.PositiveSmallIntegerField(blank=True, null=True,  default=0)
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True) 

    def send_discord_notification(self):
        if self.order.status == 'Extend':
            return print('Extend Order')
        discord_webhook_url = 'https://discord.com/api/webhooks/1218965021120270336/iFQDYMWYK7Z6DReMHG6B1KJESZyGMlV2mFv_E04TzcFfZF--_0J65S6Lg9sYMNTvxaov'
        current_time = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        embed = {
            "title": "Csgo 2",
            "description": (
                f"**Order ID:** {self.order.name}\n"
                f" From {str(self.current_rank).upper()}"
                f" To {str(self.desired_rank).upper()} server {self.order.customer_server}"
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
            self.order.name = f'Csgo{self.order.id}'
        self.order.update_actual_price()
        self.order.save()
        super().save(*args, **kwargs)
        self.send_discord_notification() 

    def get_details(self):
        return f"From {str(self.current_rank).upper()} To {str(self.desired_rank).upper()}"

    def __str__(self):
        return self.get_details()
    
    
    def get_rank_value(self, *args, **kwargs):
        promo_code = f'{None},{None}'

        if self.order.promo_code != None:
            promo_code = f'{self.order.promo_code.code},{self.order.promo_code.discount_amount}'
        return f"{self.current_rank.pk},{self.current_division},{self.current_marks},{self.desired_rank.pk},{self.desired_division},{self.order.duo_boosting},{self.order.select_booster},{self.order.turbo_boost},{self.order.streaming},{0},{self.order.customer_server},{promo_code}"
                 
    def get_order_price(self):
        # Read data from JSON file
        with open('static/csgo2/data/divisions_data.json', 'r') as file:
            division_price = json.load(file)
            flattened_data = [item for sublist in division_price for item in sublist]
            flattened_data.insert(0,0)
        try:    
            promo_code_amount = self.order.promo_code.discount_amount
        except:
            promo_code_amount = 0

        current_rank = self.current_rank.id
        reached_rank = self.reached_rank.id

        # current_division = self.current_division
        # reached_division = self.reached_division

        total_percent = 0

        if self.order.duo_boosting:
            total_percent += 0.65

        if self.order.select_booster:
            total_percent += 0.10

        if self.order.turbo_boost:
            total_percent += 0.20

        if self.order.streaming:
            total_percent += 0.15


        start_division = ((current_rank-1)*1) + 1
        end_division = ((reached_rank-1)*1)+ 1

        sublist = flattened_data[start_division:end_division]

        total_sum = sum(sublist)    

        custom_price = total_sum 
        
        custom_price += (custom_price * total_percent)
        custom_price -= custom_price * (promo_code_amount/100)
        ##############################################################

        actual_price = self.order.actual_price
        main_price = self.order.price

        percent = round(actual_price / (main_price/100))

        booster_price = round(custom_price * (percent/100), 2)
        percent_for_view = round((booster_price/actual_price)* 100)
        print('percent', percent)

        # if percent_for_view > 100:
        #     percent_for_view = 100

        # if booster_price > actual_price:
        #     booster_price = actual_price

        return {"booster_price":booster_price, 'percent_for_view':percent_for_view, 'main_price': main_price-custom_price, 'percent':percent}

class Csgo2PremierOrder(models.Model):
    pass


class CsgoFaceitOrder(models.Model):
    pass