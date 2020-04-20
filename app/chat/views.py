# chat/views.py
from django.shortcuts import render

from chat.models import Room, Chat

from django.shortcuts import render


def index(request):
    rooms = Room.objects.order_by('title')
    return render(request, 'chat/index.html', {
        "rooms" : rooms,
    })

def room(request, room_name):

    room = Room.objects.get_or_create(title=room_name)
    # room.chat_set

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        "user" : request.user
    })
