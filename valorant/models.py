from django.db import models
from accounts.models import BaseOrder, Wallet
from accounts.templatetags.custom_filters import romanize_division

# Create your models here.
class ValorantRank(models.Model):
  rank_name = models.CharField(max_length=25)
  rank_image = models.ImageField(upload_to='valorant/images/', blank=True, null=True)

  def __str__(self):
    return self.rank_name
    
  def get_image_url(self):
    return f"/media/{self.rank_image}"
  
class ValorantTier(models.Model):
  rank = models.OneToOneField('ValorantRank', related_name='tier', on_delete=models.CASCADE)
  from_I_to_II = models.FloatField(default=0)
  from_II_to_III = models.FloatField(default=0)
  from_III_to_I_next = models.FloatField(default=0)

  def __str__(self):
    return f"Tiers for {self.rank.rank_name}"

class ValorantMark(models.Model):
  rank = models.OneToOneField('ValorantRank', related_name='mark', on_delete=models.CASCADE)
  marks_0_20 = models.FloatField(default=0)
  marks_21_40 = models.FloatField(default=0)
  marks_41_60 = models.FloatField(default=0)
  marks_61_80 = models.FloatField(default=0)
  marks_81_100 = models.FloatField(default=0)

  def __str__(self):
    return f"{self.rank} -> Marks 0-20 : {self.marks_0_20}, Marks 21_40 : {self.marks_21_40}, Marks 41_60 : {self.marks_41_60}, Marks 61_80 : {self.marks_61_80}, Marks 81_100 : {self.marks_81_100}"
  
class WildRiftPlacement(models.Model):
  rank_name = models.CharField(max_length=25)
  rank_image = models.ImageField(upload_to='valorant/images/', blank=True, null=True)
  price = models.FloatField()

  def __str__(self):
    return self.name
  
  def get_image_url(self):
    return f"/media/{self.rank_image}"
  
class ValorantDivisionOrder(models.Model):
  DIVISION_CHOICES = [
    (1, 'I'),
    (2, 'II'),
    (3, 'III'),
  ]
  MARKS_CHOISES = [
      (1, '0-20'),
      (2 , '21-40'),
      (3, '41-60'),
      (4, '61-80'),
      (5, '81-100')
  ]
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='valorant_division_order')
  current_rank = models.ForeignKey(ValorantRank, on_delete=models.CASCADE, default=None, related_name='current_rank',blank=True, null=True)
  reached_rank = models.ForeignKey(ValorantRank, on_delete=models.CASCADE, default=None, related_name='reached_rank',blank=True, null=True)
  desired_rank = models.ForeignKey(ValorantRank, on_delete=models.CASCADE, default=None, related_name='desired_rank',blank=True, null=True)
  current_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  reached_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  desired_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
  current_marks = models.IntegerField(choices=MARKS_CHOISES,blank=True, null=True)
  reached_marks = models.IntegerField(choices=MARKS_CHOISES,blank=True, null=True)

  choose_agents = models.BooleanField(default=False, blank=True, null=True)

  def process_name(self):
    # Split the invoice string by the hyphen ("-") delimiter
    invoice_values = self.order.invoice.split('-')

    # Extract specific values
    self.current_division = int(invoice_values[3])
    self.current_marks = int(invoice_values[4])
    self.desired_division = int(invoice_values[6])
    self.order.price = float(invoice_values[12])
    
    # Update the BaseOrder fields based on invoice_values
    self.order.duo_boosting = bool(int(invoice_values[7]))
    self.order.select_booster = bool(int(invoice_values[8]))
    self.order.turbo_boost = bool(int(invoice_values[9]))
    self.order.streaming = bool(int(invoice_values[10]))

    current_rank_id = int(invoice_values[2])
    desired_rank_id = int(invoice_values[5])


    self.current_rank = ValorantRank.objects.get(pk=current_rank_id)
    self.desired_rank = ValorantRank.objects.get(pk=desired_rank_id)
    self.reached_rank = self.current_rank
    self.reached_division = self.current_division
    self.reached_marks = self.current_marks

    if not self.order.name:
      self.order.name = f'Valo{self.order.id}'

  def save_with_processing(self, *args, **kwargs):
    self.process_name()
    self.order.update_actual_price()
    self.order.save()
    super().save(*args, **kwargs)

  def __str__(self):
    return f"Boosting From {str(self.current_rank).upper()} {self.current_division} Marks {self.current_marks} To {str(self.desired_rank).upper()} {self.desired_division}"

  
  def get_rank_value(self, *args, **kwargs):
    return f"{self.current_rank.id},{self.current_division},{self.current_marks},{self.desired_rank.id},{self.desired_division},{self.order.duo_boosting},{False},{self.order.turbo_boost},{self.order.streaming }"
    
class ValorantPlacementOrder(models.Model):
  order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='valorant_placement_order')
  last_rank = models.ForeignKey(WildRiftPlacement, on_delete=models.CASCADE, default=None, related_name='last_rank')
  number_of_match = models.IntegerField(default=5)

  choose_agents = models.BooleanField(default=False, blank=True, null=True)

  def __str__(self):
    return f"Boosting of {self.number_of_match} Placement Games With Rank {self.last_rank}"