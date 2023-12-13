from django.shortcuts import render, redirect , HttpResponse, get_object_or_404
from django.db import models
from accounts.models import BaseUser
from django.core.validators import MinValueValidator, MaxLengthValidator
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils import timezone

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
    SERVER_CHOISES = [
        (1, 'Europa'),
        (2, 'America'),
        (3, 'Asia'),
        (4, 'Africa'),
        (5, 'Australia')
    ]
    name = models.CharField(max_length=300, default='name')
    current_rank = models.ForeignKey(WildRiftRank, on_delete=models.CASCADE, default=None, related_name='current_rank',blank=True, null=True)
    reached_rank = models.ForeignKey(WildRiftRank, on_delete=models.CASCADE, default=None, related_name='reached_rank',blank=True, null=True)
    desired_rank = models.ForeignKey(WildRiftRank, on_delete=models.CASCADE, default=None, related_name='desired_rank',blank=True, null=True)
    current_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
    reached_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
    desired_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
    current_marks = models.IntegerField(choices=MARKS_CHOISES,blank=True, null=True)
    reached_marks = models.IntegerField(choices=MARKS_CHOISES,blank=True, null=True)
    price = models.FloatField(default=0,blank=True, null=True)
    actual_price = models.FloatField(default=0, blank=True, null=True)
    invoice = models.CharField(max_length=300,)
    booster_percent1 = models.IntegerField(default=50)
    booster_percent2 = models.IntegerField(default=60)
    booster_percent3 = models.IntegerField(default=70)
    booster_percent4 = models.IntegerField(default=80)
    customer = models.ForeignKey(BaseUser,null=True , blank=True, on_delete=models.CASCADE, default=None, related_name='customer_division')
    booster = models.ForeignKey(BaseUser,null=True , blank=True, on_delete=models.CASCADE, default=None, related_name='booster_division', limit_choices_to={'is_booster': True} ) 
    duo_boosting = models.BooleanField(default=False ,blank=True)
    select_booster = models.BooleanField(default=False ,blank=True)
    turbo_boost = models.BooleanField(default=False ,blank=True)
    streaming = models.BooleanField(default=False ,blank=True)
    finish_image = models.ImageField(upload_to='wildRift/images/orders', blank=True, null=True)
    is_done = models.BooleanField(default=False ,blank=True)
    is_drop = models.BooleanField(default=False ,blank=True)
    customer_gamename = models.CharField(max_length=300, blank=True, null=True)
    customer_password = models.CharField(max_length=300, blank=True, null=True)
    customer_server = models.IntegerField(choices=SERVER_CHOISES, blank=True, null=True)
    data_correct = models.BooleanField(default=False ,blank=True)
    message = models.CharField(max_length=300, null=True, blank=True)
    payer_id = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def process_name(self):
        # Split the invoice string by the hyphen ("-") delimiter
        invoice_values = self.invoice.split('-')


        # Extract specific values
        self.current_division = int(invoice_values[3])
        self.current_marks = int(invoice_values[4])
        self.desired_division = int(invoice_values[6])
        self.price = float(invoice_values[12]) 

        # 0 orr 1 to true or false
        self.duo_boosting = bool(invoice_values[7])
        self.select_booster = bool(invoice_values[8])
        self.turbo_boost = bool(invoice_values[9])
        self.streaming = bool(invoice_values[10])

        current_rank_id = int(invoice_values[2])
        desired_rank_id = int(invoice_values[5])

        self.current_rank = WildRiftRank.objects.get(pk=current_rank_id)
        self.desired_rank = WildRiftRank.objects.get(pk=desired_rank_id)
        self.reached_rank = self.current_rank
        self.reached_division = self.current_division

    
    def update_actual_price(self):
        current_time = timezone.now()

        if not self.created_at:
            self.actual_price = self.price * (self.booster_percent1 / 100)
        else:
            time_difference = (current_time - self.created_at).total_seconds() / 60

            if time_difference <= 1:
                self.actual_price = self.price * (self.booster_percent2 / 100)
            elif time_difference <= 2:
                self.actual_price = self.price * (self.booster_percent3 / 100)
            elif time_difference <= 3:
                self.actual_price = self.price * (self.booster_percent4 / 100)
            else:
                self.actual_price = self.price * (self.booster_percent4 / 100)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_booster_wallet()

    def update_booster_wallet(self):
        if self.is_done and self.booster and self.actual_price > 0:
            booster_wallet = self.booster.wallet
            booster_wallet.available_balance += self.actual_price
            booster_wallet.save()


    def save_with_processing(self, *args, **kwargs):
        self.process_name()
        self.update_actual_price()
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
    customer = models.ForeignKey(BaseUser,null=True , blank=True, on_delete=models.CASCADE, default=None, related_name='customer_placement')
    booster = models.ForeignKey(BaseUser,null=True , blank=True, on_delete=models.CASCADE, default=None, related_name='booster_placement', limit_choices_to={'is_booster': True} )
    duo_boosting = models.BooleanField(default=False ,blank=True)
    select_booster = models.BooleanField(default=False ,blank=True)
    turbo_boost = models.BooleanField(default=False ,blank=True)
    streaming = models.BooleanField(default=False ,blank=True)
    is_done = models.BooleanField(default=False ,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Boosting of {self.number_of_match} Placement Games With Rank {self.last_rank}"