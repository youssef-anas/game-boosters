from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver
from wildRift.models import WildRiftRank

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