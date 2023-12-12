from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import BaseUser

User = get_user_model()

class Room(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    customer = models.ForeignKey(BaseUser,null=True , blank=True, on_delete=models.CASCADE, default=None, related_name='customer_room', limit_choices_to={'is_booster': False})
    booster = models.ForeignKey(BaseUser,null=True , blank=True, on_delete=models.CASCADE, default=None, related_name='booster_room', limit_choices_to={'is_booster': True} ) 

    def __str__(self):
        return "Room : "+ self.name + " | Id : " + self.slug
    
    @classmethod
    def create_room_with_booster(cls,user,booster):
        room = cls(name=f'{user}-{booster}', slug=f'roomFor_{user}_{booster}')
        room.save()
        return room
    
    @classmethod
    def create_room_with_admins(cls,user):
        room = cls(name=f'{user}-admins', slug=f'roomFor_{user}_admins')
        room.save()
        return room
    
    @classmethod
    def get_all_rooms(cls):
        return cls.objects.all().order_by('-created_on')
    
    @classmethod
    def get_specific_room(cls,user,booster):
        return cls.objects.filter(name=f'{user}-{booster}').first()
    
    @classmethod
    def get_specific_admins_room(cls,user):
        return cls.objects.filter(name=f'{user}-admins').first()
    
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Message is :- "+ self.content
    
    @classmethod
    def get_last_msg(cls,room):
        last_message = cls.objects.filter(room=room).order_by('-created_on').first()
        return last_message