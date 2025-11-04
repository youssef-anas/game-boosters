import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone

logger = logging.getLogger(__name__)

# Try imports defensively to avoid hard failures if modules are missing
try:
    from accounts.models import BaseOrder, Transaction
except Exception:  # pragma: no cover
    BaseOrder = None
    Transaction = None

try:
    from leagueOfLegends.models import LeagueOfLegendsDivisionOrder
except Exception:  # pragma: no cover
    LeagueOfLegendsDivisionOrder = None

# Optional pricing model (if exists)
PricingModel = None
for dotted in (
    'games.models.Pricing',
    'pricing.models.Pricing',
):
    try:
        module_path, cls_name = dotted.rsplit('.', 1)
        module = __import__(module_path, fromlist=[cls_name])
        PricingModel = getattr(module, cls_name)
        break
    except Exception:
        continue


def _send_notification(role: str, title: str, message: str):
    channel_layer = get_channel_layer()
    if not channel_layer:
        logger.warning("Channel layer not configured; skipping notification")
        return
    group = f'notifications_{role}'
    payload = {
        'type': 'notification',
        'title': title,
        'message': message,
        'timestamp': timezone.now().isoformat(),
    }
    async_to_sync(channel_layer.group_send)(group, payload)
    logger.info(f"Notification sent: {title} → {role} :: {message}")


if BaseOrder is not None:
    @receiver(post_save, sender=BaseOrder)
    def base_order_changed(sender, instance, created, **kwargs):
        try:
            title = 'Order Created' if created else 'Order Updated'
            msg = f"Order #{instance.id} for {getattr(instance.customer, 'username', 'customer')} is {instance.status}"
            # Notify all roles
            for role in ('admin', 'booster', 'customer'):
                _send_notification(role, title, msg)
        except Exception as e:  # pragma: no cover
            logger.error(f"Error in BaseOrder signal: {e}")


if LeagueOfLegendsDivisionOrder is not None:
    @receiver(post_save, sender=LeagueOfLegendsDivisionOrder)
    def lol_progress_changed(sender, instance, created, **kwargs):
        try:
            title = 'Progress Updated'
            percent = 0
            try:
                price_info = instance.get_order_price()
                percent = price_info.get('percent_for_view', 0)
            except Exception:
                pass
            msg = f"Order #{instance.order_id} progress is now {percent}%"
            for role in ('admin', 'booster', 'customer'):
                _send_notification(role, title, msg)
        except Exception as e:  # pragma: no cover
            logger.error(f"Error in LoL signal: {e}")


if Transaction is not None:
    @receiver(post_save, sender=Transaction)
    def transaction_changed(sender, instance, created, **kwargs):
        try:
            title = 'Payment Received' if created else 'Payment Update'
            msg = f"Transaction #{instance.id} ({instance.type}) is {instance.status} for order #{getattr(instance.order, 'id', 'N/A')}"
            for role in ('admin', 'booster', 'customer'):
                _send_notification(role, title, msg)
        except Exception as e:  # pragma: no cover
            logger.error(f"Error in Transaction signal: {e}")


if PricingModel is not None:
    @receiver(post_save, sender=PricingModel)
    def pricing_changed(sender, instance, created, **kwargs):
        try:
            title = 'Pricing Created' if created else 'Pricing Changed'
            msg = f"Pricing '{getattr(instance, 'name', 'item')}' was updated"
            for role in ('admin', 'booster', 'customer'):
                _send_notification(role, title, msg)
        except Exception as e:  # pragma: no cover
            logger.error(f"Error in Pricing signal: {e}")



