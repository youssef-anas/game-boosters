from django.db import models
from accounts.models import BaseOrder, Wallet
from accounts.templatetags.custom_filters import romanize_division
import requests


class MobileLegendsRank(models.Model):
  rank_name = models.CharField(max_length=25)
  rank_image = models.ImageField(upload_to='mobile_legends/images/', blank=True, null=True)

  def __str__(self):
    return self.rank_name
    
  def get_image_url(self):
    return f"/media/{self.rank_image}"
  
class MobileLegendsTier(models.Model):
  rank = models.OneToOneField('MobileLegendsRank', related_name='tier', on_delete=models.CASCADE)
  from_V_to_IV = models.FloatField(default=0)
  from_IV_to_III = models.FloatField(default=0)
  from_III_to_II = models.FloatField(default=0)
  from_II_to_I = models.FloatField(default=0)
  from_I_to_IV_next = models.FloatField(default=0)

  def __str__(self):
    return f"Tiers for {self.rank.rank_name}"

class MobileLegendsMark(models.Model):
  rank = models.OneToOneField('MobileLegendsRank', related_name='mark', on_delete=models.CASCADE)
  marks_0_20 = models.FloatField(default=0)
  marks_21_40 = models.FloatField(default=0)
  marks_41_60 = models.FloatField(default=0)
  marks_61_80 = models.FloatField(default=0)
  marks_81_99 = models.FloatField(default=0)
  marks_series = models.FloatField(default=0)

  def __str__(self):
    return f"{self.rank} -> Marks 0-20 : {self.marks_0_20}, Marks 21_40 : {self.marks_21_40}, Marks 41_60 : {self.marks_41_60}, Marks 61_80 : {self.marks_61_80}, Marks 81_99 : {self.marks_81_99}, Marks Series : {self.marks_series}"
  
class MobileLegendsPlacement(models.Model):
  rank_name = models.CharField(max_length=25)
  rank_image = models.ImageField(upload_to='Mobile_Legends/images/', blank=True, null=True)
  price = models.FloatField()

  def __str__(self):
    return self.rank_name
  
  def get_image_url(self):
    return f"/media/{self.rank_image}"
  
class MobileLegendsDivisionOrder(models.Model):
  DIVISION_CHOICES = [
    (1, 'V'),
    (2, 'IV'),
    (3, 'III'),
    (4, 'II'),
    (5, 'I'),
  ]
  MARKS_CHOISES = [
    (1, '1 Star'),
    (2, '2 Star'),
    (3, '3 Star'),
    (4, '4 Star'),
    (5, '5 Star'),
  ]
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='mobile_legends_division_order')
  current_rank = models.ForeignKey(MobileLegendsRank, on_delete=models.CASCADE, default=None, related_name='current_rank',blank=True, null=True)
  reached_rank = models.ForeignKey(MobileLegendsRank, on_delete=models.CASCADE, default=None, related_name='reached_rank',blank=True, null=True)
  desired_rank = models.ForeignKey(MobileLegendsRank, on_delete=models.CASCADE, default=None, related_name='desired_rank',blank=True, null=True)
  current_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  reached_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  desired_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  current_marks = models.IntegerField(choices=MARKS_CHOISES,blank=True, null=True)
  reached_marks = models.IntegerField(choices=MARKS_CHOISES,blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add =True)
  choose_champions = models.BooleanField(default=True, blank=True, null=True)

  def save_with_processing(self, *args, **kwargs):
    self.order.game_id = 8
    self.order.game_name = 'mobile legends'
    self.order.game_type = 'D'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'LOL{self.order.id}'
    self.order.update_actual_price()
    self.order.save()
    super().save(*args, **kwargs)
    # self.send_discord_notification()
    
  def get_details(self):
    return f"From {str(self.current_rank).upper()} {romanize_division(self.current_division)} {'0-20' if self.current_marks == 0 else ('21-40' if self.current_marks == 1 else ('41-60' if self.current_marks == 2 else ('61-80' if self.current_marks == 3 else ('81-99' if self.current_marks == 4 else 'SERIES'))))} LP To {str(self.desired_rank).upper()} {romanize_division(self.desired_division)}"


  def __str__(self):
    return self.get_details()
  
  def get_rank_value(self, *args, **kwargs):
    return f"{self.current_rank.id},{self.current_division},{self.current_marks},{self.desired_rank.id},{self.desired_division},{self.order.duo_boosting},{False},{self.order.turbo_boost},{self.order.streaming },{self.choose_champions}"
    
class MobileLegendsPlacementOrder(models.Model):
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='mob_leg_placement_order')
  last_rank = models.ForeignKey(MobileLegendsPlacement, on_delete=models.CASCADE, default=None, related_name='mob_leg_last_rank')
  number_of_match = models.IntegerField(default=5)

  choose_champions = models.BooleanField(default=False, blank=True, null=True)

  def save_with_processing(self, *args, **kwargs):
    self.order.game_id = 8
    self.order.game_name = 'mobile legends'
    self.order.game_type = 'P'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'mob-leg{self.order.id}'
    self.order.update_actual_price()
    self.order.save()
    super().save(*args, **kwargs)

  def get_details(self):
    return f"Boosting of {self.number_of_match} Placement Games With Rank {self.last_rank}"

  def __str__(self):
    return self.get_details()