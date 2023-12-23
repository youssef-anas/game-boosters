from django.shortcuts import render, redirect , HttpResponse, get_object_or_404
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxLengthValidator
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from accounts.models import BaseOrder

User = settings.AUTH_USER_MODEL
# # Create your models here.

# class Wild_rift_rc(models.Model):
#     # rc = rank_price
#     iron_rc = models.FloatField(default=2.54)
#     bronze_rc = models.FloatField(default=4.15)
#     silver_rc = models.FloatField(default=5.80)
#     gold_rc = models.FloatField(default=9.06)
#     gold_rc_from_II_to_I = models.FloatField(default=12.95)
#     gold_rc_from_I_to_platinum = models.FloatField()
#     platinum_rc = models.FloatField(default=12.95)
#     platinum_rc_from_I_to_emerald = models.FloatField(default=19.42)
#     emerald_rc = models.FloatField(default=27.78)
#     diamond_rc_from_IV_to_III = models.FloatField(default=48.12)
#     diamond_rc_from_III_to_II = models.FloatField(default=53.45)
#     diamond_rc_from_II_to_I = models.FloatField(default=76.80)
#     diamond_rc_from_I_to_master = models.FloatField(default=85.32)

#     def save(self, *args, **kwargs):
#         self.Gold_rc_from_I_to_Platinum = self.Gold_rc_from_II_to_I
#         super().save(*args, **kwargs)


# class Wild_rift_mc():
#     # mc = mark cost 
#     iron_mc = models.FloatField(default=0.38) # 6.70
#     bronze_mc = models.FloatField(default=0.41) # 10.10
#     silver_mc = models.FloatField(default=0.58) # 10.00
#     gold_mc = models.FloatField(default=0.88) # 10.29
#     platinum_mc = models.FloatField(default=1.04) # 12.451
#     platinum_mc_from_I_to_emerald = models.FloatField(default=1.50)# 12.946
#     emerald_mc = models.FloatField(default=1.94)

# wildRift/models.py



class WildRiftRank(models.Model):
    rank_name = models.CharField(max_length=25)
    rank_image = models.ImageField(upload_to='wildRift/images/', blank=True, null=True)
    customer_show = models.BooleanField(default=False ,blank=True)
    booster_show = models.BooleanField(default=False ,blank=True)

    def __str__(self):
        return self.rank_name
    
    def get_image_url(self):
        return f"/media/{self.rank_image}"
    
# @receiver(post_migrate)
# def create_default_ranks(sender, **kwargs):
#     if sender.name == 'your_app_name':  # Replace 'your_app_name' with the actual name of your app
#         WildRiftRank.objects.get_or_create(rank_name='Default Rank 1', rank_image='path/to/default_image_1.jpg')
#         WildRiftRank.objects.get_or_create(rank_name='Default Rank 2', rank_image='path/to/default_image_2.jpg')

class WildRiftTier(models.Model):
    rank = models.OneToOneField('WildRiftRank', related_name='tier', on_delete=models.CASCADE)
    from_IV_to_III = models.FloatField(default=0)
    from_III_to_II = models.FloatField(default=0)
    from_II_to_II = models.FloatField(default=0)
    from_I_to_IV_next = models.FloatField(default=0)

    def __str__(self):
        return f"Tiers for {self.rank.rank_name}"

class WildRiftMark(models.Model):
    class MarkChoices(models.IntegerChoices):
        MARK_2 = 2, '2 Marks'
        MARK_3 = 3, '3 Marks'
        MARK_4 = 4, '4 Marks'
        MARK_5 = 5, '5 Marks'
        MARK_6 = 6, '6 Marks'

    rank = models.OneToOneField('WildRiftRank', related_name='mark', on_delete=models.CASCADE)
    tier = models.OneToOneField(WildRiftTier, related_name='tier_mark', on_delete=models.CASCADE)
    mark_number = models.IntegerField(choices=MarkChoices.choices)
    mark_1 = models.FloatField(default=0)
    mark_2 = models.FloatField(default=0)
    mark_3 = models.FloatField(default=0)
    mark_4 = models.FloatField(default=0)
    mark_5 = models.FloatField(default=0)
    mark_6 = models.FloatField(default=0)



    def __str__(self):
        return f"Mark {self.mark_number} for Tiers: {self.tier} in Rank: {self.rank.rank_name}"
    

class WildRiftPlacement(models.Model):
    name = models.CharField(max_length=25)
    image = models.ImageField(upload_to='wildRift/images/', blank=True, null=True)
    price = models.FloatField()


    def __str__(self):
        return self.name
    
    def get_image_url(self):
        return f"/media/{self.image}"
    
class WildRiftDivisionOrder(models.Model):
    DIVISION_CHOICES = [
        (1, 'IV'),
        (2, 'III'),
        (3, 'II'),
        (4, 'I'),
    ]
    MARKS_CHOISES = [
        (0 , '0 Marks'),
        (1 , '1 Marks'),
        (2 , '2 Marks'),
        (3 , '3 Marks'),
        (4 , '4 Marks'),
        (5 , '5 Marks'),
        (6 , '6 Marks'),
    ]
    order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='base_order')
    current_rank = models.ForeignKey(WildRiftRank, on_delete=models.CASCADE, default=None, related_name='current_rank',blank=True, null=True)
    reached_rank = models.ForeignKey(WildRiftRank, on_delete=models.CASCADE, default=None, related_name='reached_rank',blank=True, null=True)
    desired_rank = models.ForeignKey(WildRiftRank, on_delete=models.CASCADE, default=None, related_name='desired_rank',blank=True, null=True)
    current_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
    reached_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
    desired_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
    current_marks = models.IntegerField(choices=MARKS_CHOISES,blank=True, null=True)
    reached_marks = models.IntegerField(choices=MARKS_CHOISES,blank=True, null=True)

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

        self.current_rank = WildRiftRank.objects.get(pk=current_rank_id)
        self.desired_rank = WildRiftRank.objects.get(pk=desired_rank_id)
        self.reached_rank = self.current_rank
        self.reached_division = self.current_division
        self.reached_marks = self.current_marks

        if not self.order.name:
            self.order.name = f'WR{self.order.id}'



    def save_with_processing(self, *args, **kwargs):
        self.process_name()
        self.order.update_actual_price()
        self.order.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Boosting From {self.current_rank} {self.current_division} Marks {self.current_marks} To {self.desired_rank} {self.desired_division}"
    
class WildRiftPlacementOrder(models.Model):
    last_rank = models.ForeignKey(WildRiftPlacement, on_delete=models.CASCADE, default=None, related_name='last_rank')
    number_of_match = models.IntegerField(default=5)
    price = models.FloatField(default=0)
    invoice = models.FloatField(default=0)
    booster_percent1 = models.IntegerField(default=50)
    booster_percent2 = models.IntegerField(default=60)
    booster_percent3 = models.IntegerField(default=70)
    booster_percent4 = models.IntegerField(default=80)
    customer = models.ForeignKey(User,null=True , blank=True, on_delete=models.CASCADE, default=None, related_name='customer_placement')
    booster = models.ForeignKey(User,null=True , blank=True, on_delete=models.CASCADE, default=None, related_name='booster_placement', limit_choices_to={'is_booster': True} )
    duo_boosting = models.BooleanField(default=False ,blank=True)
    select_booster = models.BooleanField(default=False ,blank=True)
    turbo_boost = models.BooleanField(default=False ,blank=True)
    streaming = models.BooleanField(default=False ,blank=True)
    is_done = models.BooleanField(default=False ,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Boosting of {self.number_of_match} Placement Games With Rank {self.last_rank}"