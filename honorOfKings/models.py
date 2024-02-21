from django.db import models
from accounts.models import BaseOrder, Wallet
from accounts.templatetags.custom_filters import romanize_division

# Create your models here.
class HonorOfKingsRank(models.Model):
  rank_name = models.CharField(max_length=25)
  rank_image = models.ImageField(upload_to='hok/images/', blank=True, null=True)

  def __str__(self):
    return self.rank_name
    
  def get_image_url(self):
    return f"/media/{self.rank_image}"
  
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
  star_4 = models.FloatField(default=0)
  star_5 = models.FloatField(default=0)

  def __str__(self):
    return f"{self.rank} -> Stars 1: {self.start_1}, Stars 2: {self.start_2}, Stars 3: {self.start_3}, Stars 4: {self.start_4}, Stars 5: {self.start_5}"
  
class HonorOfKingsDivisionOrder(models.Model):
  DIVISION_CHOICES = [
    (1, 'V'),
    (2, 'IV'),
    (3, 'III'),
    (4, 'II'),
    (5, 'I'),
  ]
  MARKS_CHOISES = [
    (0, '1'),
    (1, '2'),
    (2, '3'),
    (3, '4'),
    (4, '5'),
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

  def save_with_processing(self, *args, **kwargs):
    self.order.game_id = 7
    self.order.game_name = 'hok'
    self.order.game_type = 'D'
    self.order.details = self.get_details()
    if not self.order.name:
      self.order.name = f'HOK{self.order.id}'
    self.order.update_actual_price()
    self.order.save()
    super().save(*args, **kwargs)
    # self.send_discord_notification()
    
  def get_details(self):
    return f"From {str(self.current_rank).upper()} {romanize_division(self.current_division)} {'3' if self.current_marks == 0 else ('2' if self.current_marks == 1 else '1')} STAR To {str(self.desired_rank).upper()} {romanize_division(self.desired_division)}"

  def __str__(self):
    return self.get_details()
  
  def get_rank_value(self, *args, **kwargs):
    return f"{self.current_rank.id},{self.current_division},{self.current_marks},{self.desired_rank.id},{self.desired_division},{self.order.duo_boosting},{False},{self.order.streaming}"