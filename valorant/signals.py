from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ValorantDivisionOrder


@receiver(post_save, sender=ValorantDivisionOrder)
def create_wildrift_tier(sender, instance, created, **kwargs):
    if created:
        if not instance.reached_rank:
            instance.reached_rank = instance.current_rank
        if not instance.reached_division:
            instance.reached_division = instance.current_division
        if not instance.reached_marks:
            instance.reached_marks = instance.current_marks
        instance.save()    
