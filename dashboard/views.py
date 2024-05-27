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
        admins_chat_slug = f'roomFor-{base_order.customer}-admins-{base_order.name}'

        admins_room = Room.objects.get(slug=admins_chat_slug)
        admins_messages = Message.objects.filter(room=admins_room)

        game_order = base_order.related_order
        
        # Chat with booster
        specific_room = Room.get_specific_room(base_order.customer, base_order.name)
        slug = specific_room.slug if specific_room else None
        if slug:
            room = Room.objects.get(slug=slug)
            chat_messages=Message.objects.filter(room=room) 
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
        return  HttpResponse("error on creating chat")
    return  HttpResponse("error on order")
