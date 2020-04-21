# chat/views.py
from django.shortcuts import render

from chat.models import Room, Chat

from django.shortcuts import render


def index(request):
    rooms = Room.objects.order_by('title')
    return render(request, 'chat/index.html', {
        "rooms": rooms,
    })


def room(request, room_name):
    room, _ = Room.objects.get_or_create(title=room_name)
    print('room_view', room)
    # room.chat_set
    chat_history = Chat.objects.filter(room__id=room.id).order_by('created_date')
    print(chat_history)
    # who = Chat.objects.filter(room__id=room.id)
    log_list = list()
    for log in chat_history:
        print(log.log, log.to_user_id)
        log_list.append(log.log)

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'user': request.user,
        'log_list': log_list,
    })
