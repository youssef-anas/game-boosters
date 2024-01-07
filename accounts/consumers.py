import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from accounts.models import BaseOrder
from accounts.order_creator import live_orders

class OrderConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'orders'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        all_orders_dict= live_orders()

        self.accept()
        self.send(text_data=json.dumps({
            'type':'order',
            'order':all_orders_dict,
        }))

    def order_list(self, event):
        order = event['order']
        self.send(text_data=json.dumps({
            'type':'order',
            'order': order,
        }))     

    # # # #    to receive message from js and auto send to others    

    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     order = text_data_json['order']
    #     user = text_data_json['user']
    #     order_with_user =[order,user]

    #     # self.send(text_data=json.dumps({
    #     #     'type':'order',
    #     #     'order':order,
    #     # }))

    #     async_to_sync(self.channel_layer.group_send)(
    #         self.room_group_name,
    #         {
    #             'type':'order_list',
    #             'order':'hi'
    #         }
    #     )
        
