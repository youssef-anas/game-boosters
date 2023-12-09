from django.shortcuts import render, HttpResponse
from .models import *
from django.contrib.auth import get_user_model

user = get_user_model()
def rooms(request):
    rooms= Room.get_all_rooms()
    last_messages = {}

    for room in rooms:
        last_message = Message.objects.filter(room=room).order_by('-created_on').first()
        last_messages[room.name] = {
            'last_message': last_message,
            'slug': room.slug,
        }
        
    return render(request, "MyChats.html",{
        "rooms":rooms,
        'user':user,
        "last_messages":last_messages
    })

def room(request,slug):
    room = Room.objects.get(slug=slug)
    room_name=Room.objects.get(slug=slug)
    messages=Message.objects.filter(room=Room.objects.get(slug=slug))
    print(room_name)
    
    return render(request, "Chat.html",{
        'room_name':room_name,
        "slug":slug,
        'messages':messages,
        'user':user,
        'room':room,
    })
    


########################### To create a room:: ###########################
# user = get_user_model()
# booster_user = user.objects.get(username='booster')
# isRoomExist = Room.get_specific_room(request.user,booster_user)
# if not isRoomExist:
#     new_room = Room.create_room(request.user, booster_user)
# else:
#     return HttpResponse('not valid')