import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from accounts.models import BaseOrder
from leagueOfLegends.models import LeagueOfLegendsDivisionOrder
from accounts.models import Transaction

logger = logging.getLogger(__name__)

class OrderSyncConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time order synchronization.
    Subscribes to updates by order ID and broadcasts order changes.
    """
    
    async def connect(self):
        """Handle WebSocket connection"""
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.group_name = f'order_{self.order_id}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send initial order data
        order_data = await self.get_order_data(self.order_id)
        if order_data:
            await self.send(text_data=json.dumps({
                'type': 'order.update',
                **order_data
            }))
        
        logger.info(f"WebSocket connected for order {self.order_id}")
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        logger.info(f"WebSocket disconnected for order {self.order_id}")
    
    async def order_update(self, event):
        """
        Receive message from room group and send to WebSocket.
        This is called when a group message is sent.
        """
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'order.update',
            'order_id': event.get('order_id'),
            'status': event.get('status'),
            'progress': event.get('progress'),
            'booster_price': event.get('booster_price'),
            'actual_price': event.get('actual_price'),
            'booster_id': event.get('booster_id'),
            'booster_username': event.get('booster_username'),
            'reached_rank': event.get('reached_rank'),
            'reached_division': event.get('reached_division'),
            'reached_marks': event.get('reached_marks'),
            'message': event.get('message'),
            'timestamp': event.get('timestamp'),
        }))
    
    @database_sync_to_async
    def get_order_data(self, order_id):
        """
        Fetch order data from database.
        Returns a dictionary with order information.
        """
        try:
            order = BaseOrder.objects.get(id=order_id)
            
            # Get progress information for League of Legends orders
            progress_data = {}
            booster_price = None
            reached_rank = None
            reached_division = None
            reached_marks = None
            
            # Try to get League of Legends specific order data
            try:
                lol_order = LeagueOfLegendsDivisionOrder.objects.get(order=order)
                price_info = lol_order.get_order_price()
                booster_price = str(price_info.get('booster_price', 0))
                progress_data['percent_for_view'] = price_info.get('percent_for_view', 0)
                
                # Get reached rank/division info
                if lol_order.reached_rank:
                    reached_rank = str(lol_order.reached_rank.rank_name)
                reached_division = lol_order.reached_division
                reached_marks = lol_order.reached_marks
            except LeagueOfLegendsDivisionOrder.DoesNotExist:
                # If not a LoL order, try to get progress from BaseOrder
                if hasattr(order, 'lol_division_order'):
                    lol_order = order.lol_division_order
                    price_info = lol_order.get_order_price()
                    booster_price = str(price_info.get('booster_price', 0))
                    progress_data['percent_for_view'] = price_info.get('percent_for_view', 0)
            
            # Get booster information
            booster_id = None
            booster_username = None
            if order.booster:
                booster_id = order.booster.id
                booster_username = order.booster.username
            
            return {
                'order_id': order.id,
                'status': order.status,
                'progress': progress_data.get('percent_for_view', 0),
                'booster_price': booster_price or str(order.actual_price),
                'actual_price': str(order.actual_price),
                'booster_id': booster_id,
                'booster_username': booster_username,
                'reached_rank': reached_rank,
                'reached_division': reached_division,
                'reached_marks': reached_marks,
                'message': order.message,
                'timestamp': order.updated_at.isoformat() if order.updated_at else None,
            }
        except BaseOrder.DoesNotExist:
            logger.error(f"Order {order_id} not found")
            return None
        except Exception as e:
            logger.error(f"Error fetching order data for {order_id}: {str(e)}")
            return None



