from django.db import models
from accounts.models import BaseOrder
import requests
from django.core.exceptions import ValidationError
import json
import ast

class WorldOfWarcraftRank(models.Model):
  rank_name = models.CharField(max_length=25)
  rank_image = models.ImageField(upload_to='wow/images/', blank=True, null=True)
  # start_RP = models.PositiveIntegerField(null=True)
  # end_RP = models.PositiveIntegerField(null=True)

  def __str__(self):
    return self.rank_name
    
  def get_image_url(self):
    if self.rank_image:
      return self.rank_image.url
    return None
    
  
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

class WorldOfWarcraftRpsPrice(SingletonModel):
  price_of_2vs2 = models.FloatField(default=1)
  price_of_3vs3 = models.FloatField(default=2)

  def __str__(self):
    return f"Price for 50 RPs is {self.price_of_2vs2} for 2vs2 , {self.price_of_3vs3} for 3vs3"
  
  def save(self, *args, **kwargs):
    self.pk = 1
    super().save(*args, **kwargs)
  
  
class WorldOfWarcraftArenaBoostOrder(models.Model):
  is_arena_2vs2 = models.BooleanField(default=True)

  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='wow_division_order')

  current_rank = models.ForeignKey(WorldOfWarcraftRank, on_delete=models.CASCADE, default=None, related_name='wow_current_rank')
  reached_rank = models.ForeignKey(WorldOfWarcraftRank, on_delete=models.CASCADE, default=None, related_name='wow_reached_rank')
  desired_rank = models.ForeignKey(WorldOfWarcraftRank, on_delete=models.CASCADE, default=None, related_name='wow_desired_rank')

  current_division = models.PositiveSmallIntegerField(default=0)
  reached_division = models.PositiveSmallIntegerField(default=0)
  desired_division = models.PositiveSmallIntegerField(default=0)

  rank1_player = models.BooleanField(default=False)
  tournament_player = models.BooleanField(default=False)
  boost_method = models.CharField(max_length=50)

  current_marks = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
  reached_marks = models.PositiveSmallIntegerField(default=0, blank=True, null=True)

  created_at = models.DateTimeField(auto_now_add =True)
  updated_at = models.DateTimeField(auto_now =True)

  def validate_division(self):
    if self.is_arena_2vs2:
      if not (self.current_division >= 0 and self.current_division <= 2200):
        raise ValidationError("Current division must be between 0 and 2200.")
    else:
      if not (self.current_division >= 0 and self.current_division <= 2500):
        raise ValidationError("Current division must be between 0 and 2500.")
        
    
  def send_discord_notification(self):
    if self.order.status == 'Extend':
      return print('Extend Order')
    discord_webhook_url = 'https://discordapp.com/api/webhooks/1209759469806821396/Sw69hAULnlb4XIEIclX_Ag-xCdinblnLcpr01UXtJDM2STpTw2hv8UqyD29qY2H01uXX'
    current_time = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    if self.is_arena_2vs2:
      arena = 'Arena 2vs2'
    else:
      arena = 'Arena 3vs3'

    embed = {
      "title": "World Of Warcraft",
      "description": (
        f"**Order ID:** {self.order.name}\n"
        f" From {self.current_division} RP To {self.desired_division} RP"
        f" {arena} Server {self.order.customer_server}"
      ),
      "color": 0xFFA500,
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
    # self.validate_division()
    self.order.game_id = 6
    self.order.game_type = 'A'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'WOW{self.order.id}'
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

    return f"{self.current_rank.pk},{self.current_division},{0},{self.desired_rank.pk},{self.desired_division},{self.order.duo_boosting},{self.order.select_booster},{self.order.turbo_boost},{self.order.streaming},{0},{self.order.customer_server},{promo_code},{0},{self.is_arena_2vs2}"
  
  def get_order_price(self):
    try:
      promo_code_amount = self.order.promo_code.discount_amount
    except:
      promo_code_amount = 0

    # Prices
    prices = WorldOfWarcraftRpsPrice.objects.all().first()
    price_of_2vs2 = prices.price_of_2vs2
    price_of_3vs3 = prices.price_of_3vs3

    MIN_DESIRED_VALUE = 50

    total_percent = 0

    if self.order.duo_boosting:
      total_percent += 0.65

    if self.order.select_booster:
      total_percent += 0.10

    if self.order.turbo_boost:
      total_percent += 0.20

    if self.order.streaming:
      total_percent += 0.15

    current_rp = self.current_division
    reached_rp = self.reached_division

    is_arena_2vs2 = self.is_arena_2vs2

    if is_arena_2vs2:
      custom_price = (reached_rp - current_rp) * (price_of_2vs2 / 50)
    else: 
      custom_price = (reached_rp - current_rp) * (price_of_3vs3 / 50)

    
    custom_price += (custom_price * total_percent)


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
  
# new games 

class WorldOfWarcraftBoss(models.Model): 
  WOW_MAP_CHOICES = (
    (1, "Vault of the Incarnates"),
    (2, "Aberrus, the Shadowed Crucible"),
    (3, "Amirdrassil, the Dream's Hope"),
  )
  map = models.PositiveSmallIntegerField(choices=WOW_MAP_CHOICES)
  name = models.CharField(max_length=100, unique=True)
  price = models.FloatField(default=0)
  
  class Meta:
    unique_together = ('map', 'name')

  def __str__(self):
    return self.name
  
class WorldOfWarcraftBundle(models.Model):
  MODE_CHOICES = (
    (1, "Raid"),
    (2, "Dungeon"),
  )
  name = models.CharField(max_length=40, unique=True)
  price = models.FloatField(default=0)
  image = models.ImageField(upload_to='wow/raid/')
  mode = models.PositiveSmallIntegerField(choices=MODE_CHOICES)
  feature_1 = models.CharField(max_length=40, null=True, blank=True)
  feature_2 = models.CharField(max_length=40, null=True, blank=True)
  feature_3 = models.CharField(max_length=40, null=True, blank=True)
  feature_4 = models.CharField(max_length=40, null=True, blank=True)

  def get_image_url(self):
    if self.image:
      return self.image.url
    return None

  def __str__(self):
    return self.name
  
class WorldOfWarcraftRaidSimpleOrder(models.Model):
  WOW_MAP_CHOICES = (
    (1, "Vault of the Incarnates"),
    (2, "Aberrus, the Shadowed Crucible"),
    (3, "Amirdrassil, the Dream's Hope"),
  )
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='wow_raid_simple_order')
  map = models.PositiveSmallIntegerField(null= True, choices=WOW_MAP_CHOICES, blank=True)
  difficulty = models.FloatField()
  bosses = models.ManyToManyField(WorldOfWarcraftBoss, related_name='wow_raid_simple_order_bosses')

  loot_priority = models.BooleanField()
  boost_method = models.CharField(max_length=50)

  created_at = models.DateTimeField(auto_now_add =True)
  updated_at = models.DateTimeField(auto_now =True)

  def send_discord_notification(self):
    if self.order.status == 'Extend':
      return print('Extend Order')
    discord_webhook_url = 'https://discordapp.com/api/webhooks/1209759469806821396/Sw69hAULnlb4XIEIclX_Ag-xCdinblnLcpr01UXtJDM2STpTw2hv8UqyD29qY2H01uXX'
    current_time = self.created_at.strftime("%Y-%m-%d %H:%M:%S")

    embed = {
      "title": "World Of Warcraft",
      "description": (
        f"**Order ID:** {self.order.name}\n"
        "Test mode "
      ),
      "color": 0xFFA500,
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
    # self.validate_division()
    self.order.game_id = 6
    self.order.game_type = 'R'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'WOW{self.order.id}'
    self.order.update_actual_price()
    self.order.save()
    super().save(*args, **kwargs)
    self.send_discord_notification()

  def get_details(self):
    booses_len = self.bosses.count()
    return f"Defets {booses_len} in {self.map} map"
    
  def __str__(self):
    return self.get_details()

  def get_rank_value(self, *args, **kwargs):
    promo_code = f'{None},{None}'

    if self.order.promo_code != None:
      promo_code = f'{self.order.promo_code.code},{self.order.promo_code.discount_amount}'

    return f"{self.order.duo_boosting},{self.order.select_booster},{self.order.turbo_boost},{self.order.streaming},{0},{self.order.customer_server},{promo_code},{0},"
  
  def get_order_price(self):
    return {"booster_price": 0, 'percent_for_view': 0, 'main_price': 0, 'percent': 0.24}
  

class WorldOfWarcraftRaidBundleOrder(models.Model):
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='wow_raid_bundle_order')
  bundle = models.ForeignKey(WorldOfWarcraftBundle, on_delete=models.CASCADE, related_name='wow_raid_bundle_order_bundles')
  loot_priority = models.BooleanField()
  boost_method = models.CharField(max_length=50)

  created_at = models.DateTimeField(auto_now_add =True)
  updated_at = models.DateTimeField(auto_now =True)

  def send_discord_notification(self):
    if self.order.status == 'Extend':
      return print('Extend Order')
    discord_webhook_url = 'https://discordapp.com/api/webhooks/1209759469806821396/Sw69hAULnlb4XIEIclX_Ag-xCdinblnLcpr01UXtJDM2STpTw2hv8UqyD29qY2H01uXX'
    current_time = self.created_at.strftime("%Y-%m-%d %H:%M:%S")

    embed = {
      "title": "World Of Warcraft",
      "description": (
        f"**Order ID:** {self.order.name}\n"
        "Test mode "
      ),
      "color": 0xFFA500,
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
    # self.validate_division()
    self.order.game_id = 6
    self.order.game_type = 'RB'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'WOW{self.order.id}'
    self.order.update_actual_price()
    self.order.save()
    super().save(*args, **kwargs)
    self.send_discord_notification()

  def get_details(self):
    return f"{self.bundle.name} "
    
  def __str__(self):
    return self.get_details()

  def get_rank_value(self, *args, **kwargs):
    promo_code = f'{None},{None}'

    if self.order.promo_code != None:
      promo_code = f'{self.order.promo_code.code},{self.order.promo_code.discount_amount}'

    return f"{self.order.duo_boosting},{self.order.select_booster},{self.order.turbo_boost},{self.order.streaming},{0},{self.order.customer_server},{promo_code},{0},"
  
  def get_order_price(self):
    return {"booster_price": 0, 'percent_for_view': 0, 'main_price': 0, 'percent': 0.24}
  

class KeystonePrice(models.Model):
  price = models.FloatField()

  def __str__(self):
    return f'{self.id} | {self.price}'

class WorldOfWarcraftDungeonSimpleOrder(models.Model):
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='wow_dungeon_simple_order')
  keystone = models.IntegerField()
  keys = models.IntegerField()

  traders = models.CharField(max_length=300)
  traders_armor_type = models.CharField(max_length=300)
  map_preferred = models.CharField(max_length=300)

  timed = models.BooleanField()
  boost_method = models.CharField(max_length=300)

  # algathar_academy = models.IntegerField()
  # azure_vault = models.IntegerField()
  # brackenhide_hollow = models.IntegerField()
  # halls_of_infusion = models.IntegerField()
  # neltharus = models.IntegerField()
  # nokhud_offensive = models.IntegerField()
  # ruby_life_pools = models.IntegerField()
  # uldaman_legacy_of_tyr = models.IntegerField()

  maps = models.CharField(max_length=1000)

  created_at = models.DateTimeField(auto_now_add =True)
  updated_at = models.DateTimeField(auto_now =True)

  def send_discord_notification(self):
    pass

  def save_with_processing(self, *args, **kwargs):
    self.order.game_id = 6
    self.order.game_type = 'DU'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'WOW{self.order.id}'
    self.order.update_actual_price()
    self.order.save()
    super().save(*args, **kwargs)
    self.send_discord_notification()    

  def get_details(self):
    return f"{self.keystone} keystone {self.keys} Keys"
  
  def __str__(self):
    return self.get_details()


  def get_rank_value(self, *args, **kwargs):
    promo_code = f'{None},{None}'

    if self.order.promo_code != None:
      promo_code = f'{self.order.promo_code.code},{self.order.promo_code.discount_amount}'

    return f"{self.order.duo_boosting},{self.order.select_booster},{self.order.turbo_boost},{self.order.streaming},{0},{self.order.customer_server},{promo_code},{0},"
  
  def get_order_price(self):
    return {"booster_price": 0, 'percent_for_view': 0, 'main_price': 0, 'percent': 0.24}
  
  def get_maps_as_key_value(self):
    maps_dict = ast.literal_eval(self.maps)
    return maps_dict




class WowLevelUpPrice(models.Model):
  price = models.FloatField(default=10)

  def __str__(self) -> str:
    return f'Prise for each level: {self.price}'


class WowLevelUpOrder(models.Model):
    order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='wow_level_up_order')

    current_level = models.IntegerField(null = False, blank = True, default = 1)
    reached_level = models.IntegerField(null = True, blank = True, default = 1)
    desired_level = models.IntegerField(null = False, blank = True, default = 1)

    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)


    def save_with_processing(self, *args, **kwargs):
        self.order.game_id = 6
        self.order.game_type = 'F'
        self.order.details = self.get_details()
        # 
        if not self.order.name:
            self.order.name = f'WOW{self.order.pk}'
        self.order.update_actual_price()
        self.order.save()
        super().save(*args, **kwargs)
        # self.send_discord_notification() 

    def get_details(self):
        return f"From {str(self.current_level)} Level To {str(self.desired_level)} Level"

    def __str__(self):
        return self.get_details()
    
    def get_order_price(self):
        return {"booster_price": 0, 'percent_for_view': 0, 'main_price': 0, 'percent': 0.24}
    