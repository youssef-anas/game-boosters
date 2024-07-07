import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from accounts.models import BaseUser
from chat.models import Room, Message
from django.utils import timezone
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_slug']
        self.room_group_name = 'chat_%s' % self.room_name
        self.username = self.scope['user'].username
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name

        )
        await self.set_user_online(self.username)
        await self.accept()
        
    async def disconnect(self, close_code):
        await self.set_user_offline(self.username)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        room_name = text_data_json["room_name"]
        
        await self.save_message(message, username, room_name)     

        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "sendMessage",
                "message": message,
                "username": username,
                "room_name": room_name,
                "msg_type": 1
            }
        )
        
    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        
        await self.send(text_data=json.dumps({**event}))
    
    async def change_data(self, event):
        await self.send(text_data=json.dumps({**event}))
    
    @sync_to_async
    def save_message(self, message, username, room_name):
        user=BaseUser.objects.get(username=username)
        room=Room.objects.get(name=room_name)
        return Message.objects.create(user=user,room=room,content=message)


    @database_sync_to_async
    def set_user_online(self, username):
        user = BaseUser.objects.filter(username=username).first()
        user.is_online = True
        user.save()

    @database_sync_to_async
    def set_user_offline(self, username):
        user = BaseUser.objects.filter(username=username).first()
        user.is_online = False
        user.last_online = timezone.now()
        user.save()
