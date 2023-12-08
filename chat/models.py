from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Room(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "Room : "+ self.name + " | Id : " + self.slug
    
    @classmethod
    def create_room(cls,user,booster):
        room = cls(name=f'{user}-{booster}', slug=f'roomFor_{user}_{booster}')
        room.save()
        return room
    
    @classmethod
    def get_all_rooms(cls):
        return cls.objects.all().order_by('-created_on')
    
    @classmethod
    def get_specific_room(cls,user,booster):
        return cls.objects.filter(name=f'{user}-{booster}').first()
    
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