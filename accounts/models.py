from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from games.models import Game
from django.db.models import Avg
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from allauth.socialaccount.signals import social_account_added
# from simple_history.models import HistoricalRecords


class BaseUser(AbstractUser):
    # profile_image = models.ImageField(upload_to='accounts/images/', null=True, blank=True)
    country = CountryField(blank=True,null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    is_booster = models.BooleanField(default= False)
    is_customer = models.BooleanField(default= False)
    is_admin = models.BooleanField(default= False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_online = models.BooleanField(default = False)
    last_online = models.DateTimeField(default=timezone.now)

    activation_code = models.IntegerField(null=True,blank=True)
    activation_time = models.DateTimeField(null=True,blank=True)

    rest_password_code = models.IntegerField(null=True,blank=True)
    rest_password_time = models.DateTimeField(null=True, blank=True)

        
    # history = HistoricalRecords()

    def set_full_name(self, full_name):
        names = full_name.split()
        if len(names) > 1:
            self.first_name = names[0]
            self.last_name = " ".join(names[1:])
        elif len(names) == 1:
            self.first_name = names[0]
            self.last_name = ''

    # def get_image_url(self):
    #     if self.profile_image:
    #         return self.profile_image.url
    #     return None
    
    def get_average_rating(self):
        # Check if the user is a booster
        if self.is_booster:
            # Calculate average rating for the user
            average_rating = self.ratings_received.aggregate(avg_rating=Avg('rate'))['avg_rating'] or 0.0
            return round(average_rating,2)

        else:
            # If the user is not a booster, return None or any other appropriate value
            return 0.0

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not hasattr(self, 'wallet'):
            Wallet.objects.create(user=self)            



    def clean(self):
        super().clean()
        
        # Validation for date_of_birth
        if self.date_of_birth:
            today = date.today()
            # Calculate 18 years ago from today
            eighteen_years_ago = today - timedelta(days=18 * 365)
            
            # Check if date_of_birth is not in the future and is at least 18 years ago
            if self.date_of_birth > today:
                raise ValidationError("Date of birth cannot be in the future.")
            elif self.date_of_birth > eighteen_years_ago:
                raise ValidationError("You must be at least 18 years old.")
            
    def get_image_url(self):
        if hasattr(self, 'booster') and self.booster is not None and self.is_booster:
            if self.booster.profile_image:
                return self.booster.profile_image.url
        return None
        
@receiver(post_save, sender=BaseUser)
def create_wallet(sender, instance, created, **kwargs):
    if created :
        Wallet.objects.create(user=instance)


@receiver(social_account_added)
def update_user_email(sender, **kwargs):
    sociallogin = kwargs['sociallogin']
    if sociallogin.account.provider in ['facebook', 'google']:
        extra_data = sociallogin.account.extra_data
        if 'email' in extra_data:
            user = sociallogin.user
            user.is_customer = True
            if not user.email:
                user.email = extra_data['email']
                user.save()

    
class Wallet(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE,related_name='wallet')
    money = models.FloatField(default=0, null=True, blank=True)


    def __str__(self):
        if self.user.is_customer:
            action = 'Paid'
        else:
            action = 'Has'
        return f'{self.user.username} {action} {self.money}$'
    
class PromoCode(models.Model):
    code                = models.CharField(max_length=255, unique=True)
    description         = models.CharField(null=True, max_length=255)
    discount_amount     = models.FloatField()
    expiration_date     = models.DateField()

    is_percent          = models.BooleanField(default=False)              
    is_active           = models.BooleanField(default=True)

    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.is_percent:
            percent = 'Percent'
        else:
            percent = 'For User'
        return f'{self.code } | {percent}'
    
class BoosterPercent(models.Model):
    booster_percent1 = models.IntegerField(default=22)
    booster_percent2 = models.IntegerField(default=24)
    booster_percent3 = models.IntegerField(default=27)
    booster_percent4 = models.IntegerField(default=30)
    booster_percent5 = models.IntegerField(default=35)


class Captcha(models.Model):
    image = models.ImageField()
    value = models.CharField()

    def __str__(self) -> str:
        return self.value    
        
# Base Order
class BaseOrder(models.Model):
    SERVER_CHOICES = [
        (1, 'Europa'),
        (2, 'America'),
        (3, 'Asia'),
        (4, 'Africa'),
        (5, 'Australia'),
        (6, 'North America'),
        (7, 'South America'),
        (8, 'Middle East'),
        (9, 'KRJP'),
    ]
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Droped', 'Droped'),
        ('Extend', 'Extend'),
        ('Done', 'Done'),
        ('Continue', 'Continue'),
    ]
    GAME_TYPE = [
        ('D', 'Division'),
        ('P', 'Placement'),
        ('A', 'Arena'),      
        ('F', 'Faceit'),
        ('R', 'Raid'),      
        ('RB', 'Raid Bundle'),
        ('DU', 'Dungeon'),
        ('DB', 'Dungeon Bundle'),       
    ]
    name = models.CharField(max_length=30, null = True)
    
    details = models.CharField(max_length=300, default='no details')

    game = models.ForeignKey(Game, null=True, on_delete=models.DO_NOTHING, default=None, related_name='game')
    game_type = models.CharField(max_length=10, choices=GAME_TYPE, null=True)

    price = models.FloatField(default=0, blank=True, null=True)
    actual_price = models.FloatField(default=0, blank=True, null=True)
    real_order_price = models.FloatField() 
    money_owed = models.FloatField(default=0, blank=True, null=True)
    invoice = models.CharField(max_length=2000)

    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='New', null=True, blank=True)

    customer = models.ForeignKey(BaseUser, null=True, blank=True, on_delete=models.DO_NOTHING, default=None, related_name='customer_orders', limit_choices_to= {'is_customer': True})
    booster = models.ForeignKey(BaseUser,null=True , blank=True, on_delete=models.DO_NOTHING, default=None, related_name='booster_orders', limit_choices_to={'is_booster': True} ) 

    duo_boosting = models.BooleanField(default=False, blank=True)
    select_booster = models.BooleanField(default=False, blank=True)
    turbo_boost = models.BooleanField(default=False, blank=True)
    streaming = models.BooleanField(default=False, blank=True)

    finish_image = models.ImageField(upload_to='orders/images/', blank=True, null=True) # TODO not wildRift folder 
    is_done = models.BooleanField(default=False, blank=True)
    is_drop = models.BooleanField(default=False, blank=True)
    is_extended = models.BooleanField(default=False, blank=True)

    customer_gamename = models.CharField(max_length=300, default='')
    customer_password = models.CharField(max_length=300, blank=True, default='')
    customer_username = models.CharField(max_length=300, default='')
    customer_server = models.CharField(max_length=300, blank=True, null=True)

    data_correct = models.BooleanField(default=False, blank=True)
    message = models.CharField(max_length=300, null=True, blank=True)

    payer_id = models.CharField(blank=True, null=True, max_length=255)

    promo_code = models.ForeignKey(PromoCode, on_delete=models.DO_NOTHING, null= True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # this will save relation of order (:
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING, null= True)
    object_id = models.PositiveIntegerField(null =True)
    related_order = GenericForeignKey('content_type', 'object_id')

    captcha = models.ForeignKey(Captcha, on_delete=models.SET_NULL, null=True, related_name='order')

    # Pause
    pause = models.BooleanField(default=False, blank=True)
    approved = models.BooleanField(default=False, blank=True)
    wins_number = models.PositiveSmallIntegerField(blank=True, default=0)

    def update_actual_price(self):
        """
        Updates the actual price based on certain conditions and calculates various parameters.
        Returns a dictionary containing time, price, progress, and extra.
        """
        current_time = timezone.now()

        try:
            booster_percent = BoosterPercent.objects.all().first()
        except BoosterPercent.DoesNotExist:
            # Handle the case where BoosterPercent with pk=1 doesn't exist
            booster_percent = None

        if not booster_percent:
            # Handle the scenario where booster_percent is not available
            return {'time': -1, 'price': self.actual_price, 'progress': 5, 'extra': 0}

        percent1 = booster_percent.booster_percent1
        percent2 = booster_percent.booster_percent2
        percent3 = booster_percent.booster_percent3
        percent4 = booster_percent.booster_percent4
        percent5 = booster_percent.booster_percent5

        if self.turbo_boost:
            self.actual_price = round(self.real_order_price * (percent5 / 100), 2)
            self.save()
            return {'time': -1, 'price': self.actual_price, 'progress': 5, 'extra': 0}
        
        # if self.status == 'Continue':
        #     

        time_difference = (current_time - self.created_at).total_seconds() if self.created_at else None

        if time_difference is None:
            self.actual_price = round(self.real_order_price * (percent1 / 100), 2)
        elif time_difference <= 60:
            self.actual_price = round(self.real_order_price * (percent1 / 100), 2)
            next_price = round(self.real_order_price * (percent2 / 100), 2)
            extra = round(next_price - self.actual_price, 2)
            data = {'time': int(60 - time_difference), 'price': self.actual_price, 'progress': 1, 'extra': extra}
        elif time_difference <= 180:
            self.actual_price = round(self.real_order_price * (percent2 / 100), 2)
            next_price = round(self.real_order_price * (percent3 / 100), 2)
            extra = round(next_price - self.actual_price, 2)
            data = {'time': int(180 - time_difference), 'price': self.actual_price, 'progress': 2, 'extra': extra}
        elif time_difference <= 900:
            self.actual_price = round(self.real_order_price * (percent3 / 100), 2)
            next_price = round(self.real_order_price * (percent4 / 100), 2)
            extra = round(next_price - self.actual_price, 2)
            data = {'time': int(900 - time_difference), 'price': self.actual_price, 'progress': 3, 'extra': extra}
        elif time_difference <= 1800:
            self.actual_price = round(self.real_order_price * (percent4 / 100), 2)
            next_price = round(self.real_order_price * (percent5 / 100), 2)
            extra = round(next_price - self.actual_price, 2)
            data = {'time': int(1800 - time_difference), 'price': self.actual_price, 'progress': 4, 'extra': extra}
        else:
            self.actual_price = round(self.real_order_price * (percent5 / 100), 2)
            data = {'time': -1, 'price': self.actual_price, 'progress': 5, 'extra': 0}

        self.save()
        return data 

    def save(self, *args, **kwargs):
        self.update_booster_wallet()
        super().save(*args, **kwargs)

    def update_booster_wallet(self):
        if self.is_done and self.game_type in ['R', 'RB', 'DU', 'DB']:
            Transaction.objects.create (
                    user=self.booster,
                    amount=round(self.actual_price, 2),
                    order=self,
                    status='Done',  
                    type='DEPOSIT',
                    notice=f'{self.details} - {self.game.name}'
                )
            booster_wallet = self.booster.wallet
            booster_wallet.money += self.actual_price
            return booster_wallet.save()
        
        if (self.is_done or self.is_drop) and not self.is_extended and self.booster and self.money_owed != 0:
            booster_wallet = self.booster.wallet
            booster_wallet.money += self.money_owed
            booster_wallet.save()
            if self.is_drop :
                Transaction.objects.create (
                    user=self.booster,
                    amount=round(self.money_owed, 2),
                    order=self,
                    status='Drop',  
                    type='DEPOSIT',
                    notice=f'{self.details} - {self.game.name}'
                )
            else :
                Transaction.objects.create (
                    user=self.booster,
                    amount=round(self.money_owed, 2),
                    order=self,
                    status='Done',  
                    type='DEPOSIT',
                    notice=f'{self.details} - {self.game.name}'
                )

    def customer_wallet(self):        
        Transaction.objects.create (
            user=self.customer,
            amount=round(self.price, 2),
            order=self,
            status='New',  
            type='WITHDRAWAL',
            notice=f'{self.details} - {self.game.name}'
        )

    def __str__(self):
        return f'{self.customer} have [{self.game}] order - {self.details}'

class Tip_data(models.Model):
    payer_id            = models.CharField(max_length=255, null=True)
    invoice             = models.TextField(max_length=255)

    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.payer_id    
    
    @classmethod
    def create_tip(cls, invoice, payer_id) :
        return cls.objects.create(invoice=invoice, payer_id=payer_id)
        

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
    ]
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Drop', 'Drop'),
        ('Extend', 'Extend'),
        ('Done', 'Done'),
        ('Tip', 'Tip')
    ]
    user = models.ForeignKey(BaseUser, on_delete=models.PROTECT)
    amount = models.FloatField(default=0)
    order = models.ForeignKey(BaseOrder, on_delete=models.PROTECT, related_name='from_order', null=True, blank=True)
    notice = models.TextField(default='_', max_length=100)
    status = models.CharField(max_length=100,choices=STATUS_CHOICES, default='New')
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    tip = models.ForeignKey(Tip_data, related_name='tip', on_delete=models.PROTECT, null=True, blank=True) 

    def __str__(self):
        return f'{self.user.username} {self.type} {self.amount}$'

import secrets

class TokenForPay(models.Model):
    user                = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    token               = models.CharField(max_length=255, unique=True)
    invoice             = models.CharField(max_length=2000, unique=True, null=True)
    game_info           = models.TextField(max_length=2000)
    is_paid             = models.BooleanField(default=False)

    content_type        = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s token"
    
    @classmethod
    def get_token(cls, token):
        try:
            return cls.objects.get(token=token)
        except cls.DoesNotExist:
            return None

    @classmethod
    def delete_token(cls, token):
        try:
            cls.objects.get(token=token).delete()
            return None     
        except cls.DoesNotExist:
            return None    
        
    @classmethod
    def create_token_for_pay(cls, user, game_info, model):
        token = secrets.token_hex(14)
        return TokenForPay.objects.create(user=user, token=token, game_info=game_info, content_type=ContentType.objects.get_for_model(model))
