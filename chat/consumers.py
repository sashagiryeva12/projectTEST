import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
from channels.db import database_sync_to_async 

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.group_name = f'room_{self.room_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        
        user = self.scope["user"]

        await self.save_message(user.id, message)

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user.username,
                "is_teacher": user.is_teacher()
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "user": event["user"],
            "is_teacher": event["is_teacher"]
        }))

    @database_sync_to_async
    def save_message(self, user_id, text):
        room = Room.objects.get(id=self.room_id)
        user = StUser.objects.get(id=user_id)

        Message.objects.create(
            room=room,
            user=user,
            text=text
        )