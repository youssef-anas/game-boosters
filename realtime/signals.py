import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from accounts.models import BaseOrder, Transaction
from leagueOfLegends.models import LeagueOfLegendsDivisionOrder
from django.utils import timezone

logger = logging.getLogger(__name__)

# Get channel layer
channel_layer = get_channel_layer()

def send_order_update_to_group(order, extra_data=None):
    """
    Helper function to send order update to WebSocket group.
    """
    if not channel_layer:
        logger.warning("Channel layer not configured, skipping WebSocket update")
        return
    
    try:
        order_id = order.id
        group_name = f"order_{order_id}"
        
        # Get progress information for League of Legends orders
        progress = 0
        booster_price = str(order.actual_price)
        reached_rank = None
        reached_division = None
        reached_marks = None
        
        # Try to get League of Legends specific order data
        try:
            lol_order = LeagueOfLegendsDivisionOrder.objects.get(order=order)
            price_info = lol_order.get_order_price()
            booster_price = str(price_info.get('booster_price', order.actual_price))
            progress = price_info.get('percent_for_view', 0)
            
            # Get reached rank/division info
            if lol_order.reached_rank:
                reached_rank = str(lol_order.reached_rank.rank_name)
            reached_division = lol_order.reached_division
            reached_marks = lol_order.reached_marks
        except LeagueOfLegendsDivisionOrder.DoesNotExist:
            # If not a LoL order, use default progress
            progress = 100 if order.is_done else 0
        
        # Get booster information
        booster_id = None
        booster_username = None
        if order.booster:
            booster_id = order.booster.id
            booster_username = order.booster.username
        
        # Prepare message data
        message_data = {
            'type': 'order.update',
            'order_id': order_id,
            'status': order.status,
            'progress': progress,
            'booster_price': booster_price,
            'actual_price': str(order.actual_price),
            'booster_id': booster_id,
            'booster_username': booster_username,
            'reached_rank': reached_rank,
            'reached_division': reached_division,
            'reached_marks': reached_marks,
            'message': order.message,
            'timestamp': timezone.now().isoformat(),
        }
        
        # Add any extra data if provided
        if extra_data:
            message_data.update(extra_data)
        
        # Send to group
        async_to_sync(channel_layer.group_send)(
            group_name,
            message_data
        )
        
        logger.info(f"Sent order update for order {order_id} to group {group_name}")
        
    except Exception as e:
        logger.error(f"Error sending order update for order {order.id}: {str(e)}", exc_info=True)


@receiver(post_save, sender=BaseOrder)
def base_order_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for BaseOrder model.
    Emits WebSocket update when order is saved.
    """
    try:
        send_order_update_to_group(instance)
    except Exception as e:
        logger.error(f"Error in base_order_post_save for order {instance.id}: {str(e)}", exc_info=True)


@receiver(post_save, sender=LeagueOfLegendsDivisionOrder)
def lol_order_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for LeagueOfLegendsDivisionOrder model.
    Emits WebSocket update when LoL order is saved.
    """
    try:
        # Send update for the related BaseOrder
        send_order_update_to_group(instance.order)
    except Exception as e:
        logger.error(f"Error in lol_order_post_save for order {instance.order.id}: {str(e)}", exc_info=True)


@receiver(post_save, sender=Transaction)
def transaction_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for Transaction model.
    Emits WebSocket update if transaction is related to an order.
    """
    try:
        if instance.order:
            # Send update for the related order
            send_order_update_to_group(instance.order, extra_data={
                'transaction_id': instance.id,
                'transaction_amount': str(instance.amount),
                'transaction_type': instance.type,
                'transaction_status': instance.status,
            })
            # Note: Email notifications are handled by accounts/signals.py to avoid duplicates
    except Exception as e:
        logger.error(f"Error in transaction_post_save for transaction {instance.id}: {str(e)}", exc_info=True)



