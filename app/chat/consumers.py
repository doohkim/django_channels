import json
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.exceptions import ClientError
from chat.utils import get_or_create_room_or_error, create_log_or_error


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # print(self.room_name)
        # room_model = await get_or_create_room_or_error(self.room_name)
        # print(room_model)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = text_data_json['message']
        room_name = text_data_json['roomName']
        try:
            user = self.scope["user"]
        except KeyError:
            raise ClientError("USER MISS")

        chat_model = await create_log_or_error(room_name, user, message)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message' : message,
                'room_name' : room_name,
                'user': self.scope['user'].username
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        room_name = event['room_name']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'room_name': room_name
        }))
