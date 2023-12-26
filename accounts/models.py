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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    money = models.FloatField(default=0, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Has {self.money}$'

    
# Base Order
class BaseOrder(models.Model):
    SERVER_CHOICES = [
        (1, 'Europa'),
        (2, 'America'),
        (3, 'Asia'),
        (4, 'Africa'),
        (5, 'Australia')
    ]
    name = models.CharField(max_length=300, null = True)
    price = models.FloatField(default=0, blank=True, null=True)
    actual_price = models.FloatField(default=0, blank=True, null=True)
    money_owed = models.FloatField(default=0, blank=True, null=True)
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
    is_extended = models.BooleanField(default=False, blank=True)
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
                self.actual_price = self.price * (self.booster_percent1 / 100)
            elif time_difference <= 2:
                self.actual_price = self.price * (self.booster_percent2 / 100)
            elif time_difference <= 3:
                self.actual_price = self.price * (self.booster_percent3 / 100)
            else:
                self.actual_price = self.price * (self.booster_percent4 / 100)
    
    def get_time_difference_before_final_price(self):
        current_time = timezone.now()
        time_difference = (current_time - self.created_at).total_seconds()
        
        if time_difference <= 60:
            return int(60-time_difference)
        elif time_difference <= 120:
            return int(120-time_difference)
        elif time_difference <= 180:
            return int(180-time_difference)
        elif time_difference <= 240:
            return int(240-time_difference)
        else:
            return 'Time is up'
        

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_booster_wallet()

    def update_booster_wallet(self):
        if (self.is_done or self.is_drop) and not self.is_extended and self.booster and self.money_owed > 0:
            booster_wallet = self.booster.wallet
            booster_wallet.money += self.money_owed
            booster_wallet.save()

            from booster.models import Transaction
            booster_instance = self.booster.user 
            if self.is_drop :
                Transaction.objects.create (
                    user=booster_instance,
                    amount=self.money_owed,
                    order=self,
                    status=0,  
                    type='DEPOSIT'
                )
            else :
                Transaction.objects.create (
                    user=booster_instance,
                    amount=self.money_owed,
                    order=self,
                    status=1,  
                    type='DEPOSIT'
                )
      
 

    def __str__(self):
        return f'{self.customer} have order - cost {self.price}'
    

# ####################### Chat #######################
class Room(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    customer = models.ForeignKey(BaseUser,null=True , blank=True, on_delete=models.CASCADE, default=None, related_name='customer_room', limit_choices_to={'is_booster': False})
    booster = models.ForeignKey(BaseUser,null=True , blank=True, on_delete=models.CASCADE, default=None, related_name='booster_room', limit_choices_to={'is_booster': True} ) 
    order = models.ForeignKey(BaseOrder,null=True , blank=True, on_delete=models.CASCADE, default=None, related_name='rooms') 

    def __str__(self):
        return "Room : "+ self.name + " | Id : " + self.slug
    
    @classmethod
    def create_room_with_booster(cls,customer,booster,orderId):
        order_name = BaseOrder.objects.get(id = orderId).name
        room = cls(
                name=f'{customer}-{order_name}',
                slug=f'roomFor-{customer}-{order_name}',
                customer=customer,
                booster=booster,
                order_id=orderId
            )
        room.save()
        return room
    
    @classmethod
    def create_room_with_admins(cls,customer,orderId):
        order_name = BaseOrder.objects.get(id = orderId).name
        room = cls(
                name=f'{customer}-admins-{order_name}',
                slug=f'roomFor-{customer}-admins-{order_name}',
                customer=customer,
                booster=None,
                order_id=orderId
            )
        room.save()
        return room
    
    @classmethod
    def get_all_rooms(cls):
        return cls.objects.all().order_by('-created_on')
    
    @classmethod
    def get_specific_room(cls,customer,orderId):
        order_name = BaseOrder.objects.get(id = orderId).name
        return cls.objects.filter(name=f'{customer}-{order_name}').first()
    
    @classmethod
    def get_specific_admins_room(cls,customer,orderId):
        order_name = BaseOrder.objects.get(id = orderId).name
        return cls.objects.filter(name=f'{customer}-admins-{order_name}').first()
    
    def close_the_room(self, slug):
        room = Room.objects.filter(slug=slug).first()
        if room:
            room.active = False
            room.save()
    
    def reOpen_the_room(self, slug):
        room = Room.objects.filter(slug=slug).first()
        if room:
            room.active = True
            room.save()
        
    

class Message(models.Model):
    MSG_TYPE = [
        ('normal', 'normal'),
        ('tip', 'tip'),
    ]
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    content = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    msg_type = models.CharField(choices=MSG_TYPE, blank=True, null=True, default='normal')

    def __str__(self):
        return "Message is :- "+ self.content
    
    @classmethod
    def get_last_msg(cls,room):
        last_message = cls.objects.filter(room=room).order_by('-created_on').first()
        return last_message
    
    @classmethod
    def create_tip_message(cls, user, content, room):
        new_message = cls.objects.create(
            user=user,
            content=content,
            room=room,
            created_on=timezone.now(),
            msg_type='tip'
        )
        return new_message