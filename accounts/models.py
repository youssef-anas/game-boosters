from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
# from wildRift.models import WildRiftRank

class UserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email Field Must Be Set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class BaseUser(AbstractUser):
    country = CountryField(blank=True,null=True)
    is_booster = models.BooleanField(default= False)
    is_customer = models.BooleanField(default= False)
    is_admin = models.BooleanField(default= False)




    # customer_rooms = models.ManyToManyField('Room', related_name='customers', blank=True)

    def get_image_url(self):
        if self.image:
            return self.image.url
        return None
    
    def save(self, *args, **kwargs):
        if self.is_booster:
            super().save(*args, **kwargs)
        else:
            self.can_choose_me = False
            super().save(*args, **kwargs)
    
# @receiver(post_save, sender=BaseUser)
# def create_wallet(sender, instance, created, **kwargs):
#     if created and instance.is_booster:
#         Wallet.objects.create(user=instance)

@receiver(post_save, sender=BaseUser)
def create_wallet(sender, instance, created, **kwargs):
    print(f"Creating wallet for user {instance.email} - Created: {created}")
    if created:
        wallet, created = Wallet.objects.get_or_create(user=instance)
        print(f"Wallet created: {created}")
    
class Wallet(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE,related_name='wallet')
    available_balance = models.FloatField(default=0, null=True, blank=True)


    def __str__(self):
        return f'{self.user.username} Has {self.available_balance}$'
    
# Base Order
class BaseOrder(models.Model):
    SERVER_CHOICES = [
        (1, 'Europa'),
        (2, 'America'),
        (3, 'Asia'),
        (4, 'Africa'),
        (5, 'Australia')
    ]
    name = models.CharField(max_length=300, default='name')
    price = models.FloatField(default=0, blank=True, null=True)
    actual_price = models.FloatField(default=0, blank=True, null=True)
    invoice = models.CharField(max_length=300)
    booster_percent1 = models.IntegerField(default=50)
    booster_percent2 = models.IntegerField(default=60)
    booster_percent3 = models.IntegerField(default=70)
    booster_percent4 = models.IntegerField(default=80)
    customer = models.ForeignKey(BaseUser, null=True, blank=True, on_delete=models.CASCADE, default=None, related_name='customer_orders')
    booster = models.ForeignKey(BaseUser,null=True , blank=True, on_delete=models.CASCADE, default=None, related_name='booster_division', limit_choices_to={'is_booster': True} ) 
    duo_boosting = models.BooleanField(default=False, blank=True)
    select_booster = models.BooleanField(default=False, blank=True)
    turbo_boost = models.BooleanField(default=False, blank=True)
    streaming = models.BooleanField(default=False, blank=True)
    finish_image = models.ImageField(upload_to='wildRift/images/orders', blank=True, null=True)
    is_done = models.BooleanField(default=False, blank=True)
    is_drop = models.BooleanField(default=False, blank=True)
    customer_gamename = models.CharField(max_length=300, blank=True, null=True)
    customer_password = models.CharField(max_length=300, blank=True, null=True)
    customer_server = models.IntegerField(choices=SERVER_CHOICES, blank=True, null=True)
    data_correct = models.BooleanField(default=False, blank=True)
    message = models.CharField(max_length=300, null=True, blank=True)
    payer_id = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

    def __str__(self):
        return f'{self.customer} have order - cost {self.price}'