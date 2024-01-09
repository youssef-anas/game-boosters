from django.shortcuts import render, redirect , HttpResponse, get_object_or_404
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxLengthValidator
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from accounts.models import BaseOrder, Wallet
from accounts.templatetags.custom_filters import romanize_division
import requests
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class WildRiftRank(models.Model):
    rank_name = models.CharField(max_length=25)
    rank_image = models.ImageField(upload_to='wildRift/images/', blank=True, null=True)

    def __str__(self):
        return self.rank_name
    
    def get_image_url(self):
        return f"/media/{self.rank_image}"

class WildRiftTier(models.Model):
    rank = models.OneToOneField('WildRiftRank', related_name='tier', on_delete=models.CASCADE)
    from_IV_to_III = models.FloatField(default=0)
    from_III_to_II = models.FloatField(default=0)
    from_II_to_I = models.FloatField(default=0)
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
    order = models.OneToOneField(BaseOrder, on_delete=models.CASCADE, primary_key=True, default=None, related_name='wildrift_order')
    current_rank = models.ForeignKey(WildRiftRank, on_delete=models.CASCADE, default=None, related_name='current_rank',blank=True, null=True)
    reached_rank = models.ForeignKey(WildRiftRank, on_delete=models.CASCADE, default=None, related_name='reached_rank',blank=True, null=True)
    desired_rank = models.ForeignKey(WildRiftRank, on_delete=models.CASCADE, default=None, related_name='desired_rank',blank=True, null=True)
    current_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
    reached_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
    desired_division = models.IntegerField(choices=DIVISION_CHOICES,blank=True, null=True)
    current_marks = models.IntegerField(choices=MARKS_CHOISES,blank=True, null=True)
    reached_marks = models.IntegerField(choices=MARKS_CHOISES,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def send_discord_notification(self):
        if self.order.status == 'Extend':
            return print('Extend Order')
        discord_webhook_url = 'https://discord.com/api/webhooks/1190313898201583626/HtkVOsIBOEfj9Jl8eTO95ltrm36NVkKW-kq1a-XRPjOjC1UqXCMwy7t-s4DuOmxA5Ucs'
        current_time = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        embed = {
            "title": "Rift",
            "description": (
                f"**Order ID:** {self.order.name}\n"
                f" From {str(self.current_rank).upper()} {romanize_division(self.current_division)} Marks {self.current_marks} "
                f" {str(self.current_rank).upper()} {romanize_division(self.current_division)} Marks {self.current_marks} To {str(self.desired_rank).upper()} {romanize_division(self.desired_division)} server us" # change server next
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
        self.order.game_id = 1
        self.order.game_name = 'wildRift'
        self.order.game_type = 'D'
        self.order.details = self.get_details()
        # 
        if not self.order.name:
            self.order.name = f'WR{self.order.id}'
        self.order.update_actual_price()
        self.order.save()
        super().save(*args, **kwargs)
        self.send_discord_notification()
    
    def get_details(self):
        return f"From {str(self.current_rank).upper()} {romanize_division(self.current_division)} Marks {self.current_marks} To {str(self.desired_rank).upper()} {romanize_division(self.desired_division)}"

    def __str__(self):
        return self.get_details()
    
    
    def get_rank_value(self, *args, **kwargs):
        return f"{self.current_rank.id},{self.current_division},{self.current_marks},{self.desired_rank.id},{self.desired_division},{self.order.duo_boosting},{False},{self.order.turbo_boost},{self.order.streaming }"