# websocket/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class PropertyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract property_id from URL
        self.property_id = self.scope['url_route']['kwargs']['property_id']
        self.group_name = f'property_{self.property_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
        
        # Send welcome message
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'property_id': self.property_id,
            'message': f'Connected to property {self.property_id}'
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Echo message back
        await self.send(text_data=json.dumps({
            'type': 'echo',
            'message': message,
            'property_id': self.property_id
        }))

    # Receive message from room group
    async def property_update(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'property_update',
            'kbs_socket_info': event['kbs_socket_info']
        }))


class GuestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract guest_id from URL
        self.guest_id = self.scope['url_route']['kwargs']['guest_id']
        self.group_name = f'guest_{self.guest_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
        
        # Send welcome message
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'guest_id': self.guest_id,
            'message': f'Connected to guest {self.guest_id}'
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Echo message back
        await self.send(text_data=json.dumps({
            'type': 'echo',
            'message': message,
            'guest_id': self.guest_id
        }))

    # Receive message from room group
    async def guest_update(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'guest_update',
            'kbs_socket_info': event['kbs_socket_info']
        }))
