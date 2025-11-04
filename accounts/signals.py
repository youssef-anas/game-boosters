import logging
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import BaseOrder, Transaction
from gameBoosterss.emails.services import (
    send_manager_alert_email,
    send_client_payment_email,
    send_booster_payout_email,
    send_admin_error_email,
)

logger = logging.getLogger(__name__)


@receiver(post_save, sender=BaseOrder)
def order_manager_notifications(sender, instance: BaseOrder, created: bool, **kwargs):
    try:
        # Escalation heuristic based on status/message flags
        message = (instance.message or '').lower() if hasattr(instance, 'message') else ''
        status_value = (instance.status or '').lower() if hasattr(instance, 'status') else ''

        if 'escalat' in message or 'escalat' in status_value or getattr(instance, 'is_drop', False):
            title = 'Order Escalation'
            msg = f"Order #{instance.id} requires manager attention (status: {instance.status})."
            send_manager_alert_email(instance, title, msg)

        # Booster request: if no booster is assigned but order is active
        if not instance.booster and instance.status in ['New', 'Continue']:
            title = 'Booster Requested'
            msg = f"Order #{instance.id} requires a booster assignment."
            send_manager_alert_email(instance, title, msg)
    except Exception as e:
        logger.error(f"accounts.signals.order_manager_notifications error: {e}")


@receiver(post_save, sender=Transaction)
def transaction_email_notifications(sender, instance: Transaction, created: bool, **kwargs):
    try:
        order = instance.order
        if not order:
            return

        # Client payment confirmation
        if instance.type == 'WITHDRAWAL' and instance.status == 'Done':
            send_client_payment_email(order, instance)

        # Booster payout confirmation
        if instance.type == 'DEPOSIT' and instance.status == 'Done':
            send_booster_payout_email(order, instance)

        # Admin alert for payment issues (use 'Drop' as failure proxy)
        if instance.type == 'WITHDRAWAL' and instance.status == 'Drop':
            send_admin_error_email(
                title='Payment Failure',
                error_message=f"Transaction #{instance.id} failed for order #{order.id} ({instance.amount}$)",
                extra_context={"order": order, "transaction": instance},
            )
    except Exception as e:
        logger.error(f"accounts.signals.transaction_email_notifications error: {e}")


