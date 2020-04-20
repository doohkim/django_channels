from channels.db import database_sync_to_async

from members.models import User
from .exceptions import ClientError
from .models import Room, Chat


# This decorator turns this function from a synchronous function into an async one
# we can call from our async consumers, that handles Django DBs correctly.
# For more, see http://channels.readthedocs.io/en/latest/topics/databases.html
@database_sync_to_async
def get_or_create_room_or_error(room_name):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    # Check if the user is logged in
    # if not user.is_authenticated:
    #     raise ClientError("USER_HAS_TO_LOGIN")
    # Find the room they requested (by ID)
    try:
        room = Room.objects.get(title=room_name)
        print('get_roomm', room)
    except Room.DoesNotExist:
        raise ClientError("ROOM_INVALID")
    # Check permissions
    # if room.staff_only and not user.is_staff:
    #     raise ClientError("ROOM_ACCESS_DENIED")
    return room


@database_sync_to_async
def create_log_or_error(room_name, user, message):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    # Check if the user is logged in
    # if not user.is_authenticated:
    #     raise ClientError("USER_HAS_TO_LOGIN")
    # Find the room they requested (by ID)
    try:
        room_model = Room.objects.get(title=room_name)
        print('get_roomm', room_model)
    except Room.DoesNotExist:
        raise ClientError("ROOM_INVALID")

    try:
        user_model = User.objects.get(username=user)
        print('get_user', user)
    except User.DoesNotExist:
        raise ClientError("USER_INVALID")

    try:
        chat = Chat.objects.create(room=room_model, to_user=user_model, log=message)
        print('create_chat', chat)

    except Chat.DoesNotExist:
        raise ClientError('Chat_NOT_CREATED')

    return chat
