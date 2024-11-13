from django.db import models
from accounts.models import BaseOrder
from accounts.templatetags.custom_filters import romanize_division
import requests
import math

class Csgo2Rank(models.Model):
    rank_name = models.CharField(max_length=25)
    rank_image = models.ImageField(upload_to='csgo2/images/', blank=True, null=True)
    rank_image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.rank_name
    
    def get_image_url(self):
        return self.rank_image.url
    

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
    
def get_division_prices():
    divisions = Csgo2Tier.objects.all().order_by('id')
    divisions_data = [
        [division.from_I_to_I_next]
        for division in divisions
    ]
    return divisions_data

class Csgo2DivisionOrder(models.Model):
    order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='csgo2_division_order')
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
        self.order.game_id= 13
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
        return f"{self.current_rank.pk},{self.current_division},{self.current_marks},{self.desired_rank.pk},{self.desired_division},{self.order.duo_boosting},{self.order.select_booster},{self.order.turbo_boost},{self.order.streaming},{0},{self.order.customer_server},{promo_code},{0},{True}" # True - Refere To This Is Divison
                 
    def get_order_price(self):
        # Read data from utils file
        division_price = get_division_prices()
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
  
class Csgo2PremierRank(models.Model):
    rank_name = models.CharField(max_length = 300)
    start_range = models.IntegerField()
    end_range = models.IntegerField()

    def __str__(self):
        return self.rank_name
  
class Csgo2PremierPrice(SingletonModel):
    price_0_4999 = models.FloatField(default=5.42)
    price_5000_7999 = models.FloatField(default=6.77)
    price_8000_11999 = models.FloatField(default=11.28)
    price_12000_18999 = models.FloatField(default=16.28)
    price_19000_20999 = models.FloatField(default=30.35)
    price_21000_24999 = models.FloatField(default=37.61)
    price_25000_30000 = models.FloatField(default=60.17)

    def __str__(self):
        return f'Prices - {self.price_0_4999} - {self.price_5000_7999} - {self.price_8000_11999} - {self.price_12000_18999} - {self.price_19000_20999} - {self.price_21000_24999} - {self.price_25000_30000}'

def get_premier_prices():
    premier_row = Csgo2PremierPrice.objects.all().first()
    premier_prices = [
        premier_row.price_0_4999, premier_row.price_5000_7999, premier_row.price_8000_11999, 
        premier_row.price_12000_18999, premier_row.price_19000_20999, premier_row.price_21000_24999, 
        premier_row.price_25000_30000
    ]
    return premier_prices
        

class Csgo2PremierOrder(models.Model):
    order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='csgo2_premier_order')

    current_rank = models.ForeignKey(Csgo2PremierRank, on_delete=models.PROTECT, default=None, related_name='current_rank',blank=True, null=False)

    reached_rank = models.ForeignKey(Csgo2PremierRank, on_delete=models.PROTECT, default=None, related_name='reached_rank',blank=True, null=True)

    desired_rank = models.ForeignKey(Csgo2PremierRank, on_delete=models.PROTECT, default=None, related_name='desired_rank',blank=True, null=False)

    current_division = models.PositiveSmallIntegerField(blank=True, null=False,default=1)

    reached_division = models.PositiveSmallIntegerField(blank=True, null=True,default=1)

    desired_division = models.PositiveSmallIntegerField(blank=True, null=False,default=1)

    current_marks = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    reached_marks = models.PositiveSmallIntegerField(blank=True, null=True,  default=0)

    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)

    def save_with_processing(self, *args, **kwargs):
        self.order.game_id = 13
        self.order.game_type = 'A'
        self.order.details = self.get_details()
        # 
        if not self.order.name:
            self.order.name = f'Csgo{self.order.pk}'
        self.order.update_actual_price()
        self.order.save()
        super().save(*args, **kwargs)
        # self.send_discord_notification() 

    def get_details(self):
        return f"From {str(self.current_rank).upper()} Premier To {str(self.desired_rank).upper()} Premier"

    def __str__(self):
        return self.get_details()
    
    
    def get_rank_value(self, *args, **kwargs):
        promo_code = f'{None},{None}'

        if self.order.promo_code != None:
            promo_code = f'{self.order.promo_code.code},{self.order.promo_code.discount_amount}'

        return f"{self.current_rank},{self.current_division},{0},{self.desired_rank},{self.desired_division},{self.order.duo_boosting},{self.order.select_booster},{self.order.turbo_boost},{self.order.streaming},{0},{self.order.customer_server},{promo_code},{0},{False}" # False - Refere To This Is Premier

    def get_order_price(self):  # TODO want be Edited
        MIN_DESIRED_VALUE = 500
        # Read data from utils file
        premier_prices = get_premier_prices()
        premier_prices.insert(0,0)

        price1 = round(premier_prices[1]*10,2)
        price2 = round(premier_prices[2]*6,2)
        price3 = round(premier_prices[3]*8,2)
        price4 = round(premier_prices[4]*14,2)
        price5 = round(premier_prices[5]*4,2)
        price6 = round(premier_prices[6]*8,2)
        price7 = round(premier_prices[7]*10.002,2) 
        full_price_val = [price1, price2, price3, price4, price5, price6, price7]

        def get_range_current(amount):
            MAX_LISTS = [4999, 7999, 11999, 18999, 20999, 24999, 30000]
            for idx, max_val in enumerate(MAX_LISTS, start=1):
                if amount <= max_val:
                    val = max_val - amount
                    return round(val / MIN_DESIRED_VALUE, 2), idx
            print('out_of_range')
            return None, None
            
        def get_range_desired(amount):
            MAX_LISTS = [4999, 7999, 11999, 18999, 20999, 24999, 30000]
            for idx, max_val in enumerate(MAX_LISTS, start=1):
                if amount <= max_val:
                    val = amount-MAX_LISTS[idx-2]
                    return round(val / MIN_DESIRED_VALUE, 2), idx
            print('out_of_range')
            return None, None

        try:    
            promo_code_amount = self.order.promo_code.discount_amount
        except:
            promo_code_amount = 0


        total_percent = 0

        if self.order.duo_boosting:
            total_percent += 0.65

        if self.order.select_booster:
            total_percent += 0.10

        if self.order.turbo_boost:
            total_percent += 0.20

        if self.order.streaming:
            total_percent += 0.15

        current_division = self.current_division
        reached_division = self.reached_division


        curent_mmr_in_c_range, current_range = get_range_current(current_division)
        desired_mmr_in_d_range, derired_range = get_range_desired(reached_division)
        sliced_prices = full_price_val[current_range : derired_range - 1]
        sum_current = curent_mmr_in_c_range * premier_prices[current_range]
        sum_desired = desired_mmr_in_d_range * premier_prices[derired_range]
        clear_res = sum(sliced_prices)

        if current_range == derired_range:
            range_value = math.floor((reached_division - current_division ) / MIN_DESIRED_VALUE)
            custom_price = round(range_value * premier_prices[current_range], 2)
        else:
            custom_price = round(sum_current + sum_desired + clear_res,2)

        custom_price += (custom_price * total_percent)


        custom_price = round(custom_price, 2)    

        actual_price = self.order.actual_price
        main_price = self.order.real_order_price

        percent = round(actual_price / (main_price/100))

        booster_price = round(custom_price * (percent/100), 2)
        percent_for_view = round((booster_price/actual_price)* 100)

        # if percent_for_view > 100:
        #     percent_for_view = 100

        # if booster_price > actual_price:
        #     booster_price = actual_price

        return {"booster_price":booster_price, 'percent_for_view':percent_for_view, 'main_price': main_price-custom_price, 'percent':percent}
    

class CsgoFaceitPrice(SingletonModel):
    from_1_to_2 = models.FloatField(default=16.68)
    from_2_to_3 = models.FloatField(default=16.68)
    from_3_to_4 = models.FloatField(default=19.43)
    from_4_to_5 = models.FloatField(default=20.83)
    from_5_to_6 = models.FloatField(default=23.6)
    from_6_to_7 = models.FloatField(default=27.77)
    from_7_to_8 = models.FloatField(default=34.72)
    from_8_to_9 = models.FloatField(default=48.6)
    from_9_to_10 = models.FloatField(default=62.48)

    def __str__(self):
        return f'Prices - {self.from_1_to_2} - {self.from_2_to_3} - {self.from_3_to_4} - {self.from_4_to_5} - {self.from_5_to_6} - {self.from_6_to_7} - {self.from_7_to_8} - {self.from_8_to_9} - {self.from_9_to_10}'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

def get_faceit_prices():
    faceit_prices = CsgoFaceitPrice.objects.all().first()
    faceit_data = [
        0, faceit_prices.from_1_to_2, faceit_prices.from_2_to_3, faceit_prices.from_3_to_4, 
        faceit_prices.from_4_to_5, faceit_prices.from_5_to_6, faceit_prices.from_6_to_7, 
        faceit_prices.from_7_to_8, faceit_prices.from_8_to_9, faceit_prices.from_9_to_10
    ]
    return faceit_data

class CsgoFaceitOrder(models.Model):
    order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='csgo2_faceit_order')

    current_level = models.IntegerField(null = False, blank = True, default = 1)

    reached_level = models.IntegerField(null = True, blank = True, default = 1)

    desired_level = models.IntegerField(null = False, blank = True, default = 1)

    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)

    def save_with_processing(self, *args, **kwargs):
        self.order.game_id = 13
        self.order.game_type = 'F'
        self.order.details = self.get_details()
        # 
        if not self.order.name:
            self.order.name = f'Csgo{self.order.pk}'
        self.order.update_actual_price()
        self.order.save()
        super().save(*args, **kwargs)
        # self.send_discord_notification() 

    def get_details(self):
        return f"From {str(self.current_level).upper()} To {str(self.desired_level).upper()}"

    def __str__(self):
        return self.get_details()
    
    
    def get_rank_value(self, *args, **kwargs):
        promo_code = f'{None},{None}'

        if self.order.promo_code != None:
            promo_code = f'{self.order.promo_code.code},{self.order.promo_code.discount_amount}'

        return f"{self.current_level},{0},{0},{self.desired_level},{0},{self.order.duo_boosting},{self.order.select_booster},{self.order.turbo_boost},{self.order.streaming},{0},{self.order.customer_server},{promo_code}"

    def get_order_price(self):
        custom_price = self.order.money_owed

        actual_price = self.order.actual_price
        main_price = self.order.real_order_price

        percent = round(actual_price / (main_price/100))

        booster_price = self.order.money_owed

        percent_for_view = round((booster_price/actual_price)* 100)

        return {"booster_price": booster_price, 'percent_for_view':percent_for_view, 'main_price': main_price-custom_price, 'percent':percent}