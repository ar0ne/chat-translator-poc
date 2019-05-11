from channels.generic.websocket import AsyncWebsocketConsumer
from google.cloud import translate

import json
import names


class ChatConsumer(AsyncWebsocketConsumer):
    translate_client = translate.Client()

    async def connect(self):
        self.username = names.get_first_name()
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f"{self.username} joined the chat.",
                'username': self.username
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        translated_message = self.translate_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': translated_message,
                'username': self.username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        author = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': author
        }))

    def translate_message(self, message):
        translation = self.translate_client.translate(
            message,
            target_language=self.room_name)

        return translation['translatedText']

