from django.db import models
from accounts.models import BaseUser
from gameBoosterss.utils import send_mail_bootser_choose
# from gameBoosterss.smtp import MadboostEmailSender
from django.utils import timezone
import logging

class Room(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    customer = models.ForeignKey(BaseUser, blank=True, on_delete=models.DO_NOTHING, default=None, related_name='customer_room', limit_choices_to={'is_booster': False})
    booster = models.ForeignKey(BaseUser, null=True, blank=True, on_delete=models.SET_NULL, default=None, related_name='booster_room', limit_choices_to={'is_booster': True} ) 
    order_name = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    is_for_admins = models.BooleanField(null=False)

    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['name', 'customer']]


    def __str__(self):
        return self.slug
    
    @classmethod
    def get_specific_room(cls,customer,order_name):
        slug_base = f'roomFor-{customer}-{order_name}'
        slug = slug_base[:100] if len(slug_base) > 100 else slug_base
        try :
            room = cls.objects.get(slug=slug)
        except cls.DoesNotExist:
            room = None
        return room    
    
    @classmethod
    def get_specific_admins_room(cls,customer,order_name):
        slug_base = f'roomFor-{customer}-admins-{order_name}'
        slug = slug_base[:100] if len(slug_base) > 100 else slug_base
        try :
            room = cls.objects.get(slug=slug)
        except cls.DoesNotExist:
            room = None
        return room    

    @classmethod
    def create_room_with_booster(cls,customer,booster,order_name):
        room = cls.get_specific_room(customer,order_name)
        if not room :
            # Truncate order_name to fit in max_length=50
            truncated_order_name = order_name[:50] if len(order_name) > 50 else order_name
            # Create name with truncation to fit max_length=50
            name_base = f'{customer}-{truncated_order_name}'
            room_name = name_base[:50] if len(name_base) > 50 else name_base
            # Create slug with truncation to fit max_length=100
            slug_base = f'roomFor-{customer}-{order_name}'
            room_slug = slug_base[:100] if len(slug_base) > 100 else slug_base
            room = cls.objects.create(
                    name=room_name,
                    slug=room_slug,
                    customer=customer,
                    booster=booster,
                    order_name=truncated_order_name,
                    is_for_admins = False,
                )
            if booster :
                Message.create_booster_message(room=room, message="Hi, I'm your booster. It's a pleasure to work together, and I will start your order in 15 minutes or less.", sender=booster)
                try:
                    send_mail_bootser_choose(order_name, booster)
                except Exception as e:
                    # Log email error but don't fail room creation
                    logger = logging.getLogger(__name__)
                    logger.warning(f"Failed to send booster email for order {order_name}: {e}")

            else:
                Message.create_booster_message(room=room, message='One of our booster will join chat soon...', sender=BaseUser.objects.get(id=1))
        return room  
    
    @classmethod
    def create_room_with_admins(cls,customer,order_name):
        room = cls.get_specific_admins_room(customer,order_name)
        if not room :
            # Truncate order_name to fit in max_length=50
            truncated_order_name = order_name[:50] if len(order_name) > 50 else order_name
            # Create name with truncation to fit max_length=50
            # "admins-" is 7 chars, so we need to leave room for customer string and order_name
            name_base = f'{customer}-admins-{truncated_order_name}'
            room_name = name_base[:50] if len(name_base) > 50 else name_base
            # Create slug with truncation to fit max_length=100
            slug_base = f'roomFor-{customer}-admins-{order_name}'
            room_slug = slug_base[:100] if len(slug_base) > 100 else slug_base
            room = cls.objects.create(
                    name=room_name,
                    slug=room_slug,
                    customer=customer,
                    booster=None,
                    order_name=truncated_order_name,
                    is_for_admins = True,
                )
            Message.create_booster_message(room=room, message='Welcome, it`s honor for us to see you in our site', sender=BaseUser.objects.get(id=1))
            Message.create_booster_message(room=room, message='If you have any questions, do not hesitate to ask', sender=BaseUser.objects.get(id=1))
        return room
    
    @classmethod
    def get_all_rooms(cls):
        return cls.objects.all().order_by('-created_on')
    
    
    @classmethod
    def close_the_room(cls, slug):
        room = cls.objects.get(slug=slug) 
        if room:
            room.active = False
            room.save()

    @classmethod
    def reOpen_the_room(cls, slug):
        room = cls.objects.get(slug=slug)
        if room:
            room.active = True
            room.save()
        
    

class Message(models.Model):
    MSG_TYPE = (
        (1, 'normal'),
        (2, 'tip'),
        (3, 'changes'),
        (4, 'admin'),
        (5, 'refresh'),
    )
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    content = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    msg_type = models.IntegerField(choices=MSG_TYPE, default=1)
    
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
            msg_type= 2
        )
        return new_message
    
    @classmethod
    def create_change_message(cls, user, room):
        content = 'Account Details Changed.'
        new_message = cls.objects.create(
            user=user,
            content=content,
            room=room,
            msg_type= 3
        )
        return new_message
    
    @classmethod
    def create_refresh_message(cls, user, room):
        content = 'Rate Changed.'
        new_message = cls.objects.create(
            user=user,
            content=content,
            room=room,
            msg_type= 5
        )
        return new_message
    
    @classmethod
    def create_booster_message(cls, room, message, sender):
        new_message = cls.objects.create(
            user= sender,
            content=message,
            room=room,
            msg_type= 1
        )
        return new_message