from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib import messages
from accounts.models import BaseOrder
from gameBoosterss.utils import get_boosters
from django.shortcuts import redirect
from chat.models import Room, Message

# Create your views here.

@login_required
def admin_side(request, order_name):
    if not request.user.is_superuser:
        return  HttpResponse("Access Denied")
    base_order = BaseOrder.objects.filter(
            name=order_name,
        ).order_by('id').last()
    if base_order:
        # boosters = get_boosters(base_order.game.pk)
        
        # Chat with admins
        admins_room = Room.create_room_with_admins(base_order.customer, base_order.name)
        admins_chat_slug = admins_room.slug if admins_room else None
        admins_messages = Message.objects.filter(room=admins_room) if admins_room else Message.objects.none()

        game_order = base_order.related_order
        
        # Chat with booster - create room if it doesn't exist
        room = Room.create_room_with_booster(
            base_order.customer, 
            base_order.booster, 
            base_order.name
        )
        slug = room.slug if room else None
        chat_messages = Message.objects.filter(room=room) if room else Message.objects.none()
        
        context = {
            'user':request.user,
            "slug":slug,
            'messages':chat_messages,
            'room':room,
            # 'boosters':boosters,
            'order':game_order,
            'admins_room':admins_room,
            'admins_room_name':admins_room,
            'admins_messages':admins_messages,
            'admins_chat_slug':admins_chat_slug
        }    
        template_name = 'dashboard/customer_side.html'
        return render(request, template_name, context)
    return  HttpResponse("error on order")
