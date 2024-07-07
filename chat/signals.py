from django.db.models.signals import post_save
from django.dispatch import receiver
from chat.models import Message
from accounts.models import BaseOrder
from gameBoosterss.utils import send_message_mail
import threading


def send_mail_in_thread(user, order, instance):
    send_message_mail(user, order, instance)


@receiver(post_save, sender=Message)
def message_post_save(sender, instance, created, **kwargs):
    if created:
        if instance.room.slug.split('-')[-2].startswith('admins'):
            return None
        user = instance.user
        room = instance.room.order_name
        order = BaseOrder.objects.filter(name=room).last()        
        # Create and start the thread
        if user.is_booster:
            if order.customer.is_online:
                return None
        else:
            if order.booster:
                if order.booster.is_online:   
                    return None 
        email_thread = threading.Thread(target=send_mail_in_thread, args=(user, order, instance))
        email_thread.start()
