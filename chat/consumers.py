# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage
from users.models import User,Payments
from doctors.models import Doctorinfo
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.appointment_id = self.scope['url_route']['kwargs']['appointment_id']
        self.appointment = await self.get_appointment_instance(self.appointment_id)

        await self.channel_layer.group_add(
            f'chat_{self.appointment_id}',
            self.channel_name
        )

        await self.accept()
        
        # Fetch existing messages and send them to the connected client
        existing_messages = await self.get_existing_messages()
        await self.send(text_data=json.dumps({
            'type': 'existing_messages',
            'data': existing_messages,
        }))

    @database_sync_to_async
    def get_existing_messages(self):
        # Assuming you have a ChatMessage model with a 'message' field
        messages = ChatMessage.objects.filter(appointment=self.appointment)
        message_data = []
        for message in messages:
            message_data.append({
                "message":message.message,
                "sendername":message.sendername,
                "timestamp":message.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            })
        return message_data

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f'chat_{self.appointment_id}',
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sendername = data.get('sendername', 'Anonymous')

        await self.save_message(sendername, message)

        await self.channel_layer.group_send(
            f'chat_{self.appointment_id}',
            {
                'type': 'chat.message',
                'data': {
                'message': message,
                'sendername': sendername,
            },
            }
        )

    async def chat_message(self, event):
        message = event['data']['message']
        sendername = event['data']['sendername']

        await self.send(text_data=json.dumps({
            'message': message,
            'sendername': sendername,
        }))

    @classmethod
    async def send_chat_message(cls, appointment_id, message):
        await cls.send_group(f'chat_{appointment_id}', {
            'type': 'chat.message',
            'message': message,
        })

    @database_sync_to_async
    def get_appointment_instance(self, appointment_id):
        try:
            appointment = Payments.objects.get(id=appointment_id)
            return appointment
        except Payments.DoesNotExist:
            print("Failed to find the appointment")

    async def save_message(self,sendername, message):
        sender = await self.get_user_instance(self.appointment.user_id)
        receiver = await self.get_doctor_instance(self.appointment.doctor_id)
        sendername = sendername
        await self.save_message_to_db(sender, receiver, sendername, message)

    @database_sync_to_async
    def save_message_to_db(self, sender, receiver, sendername, message):
        ChatMessage.objects.create(
            sender=sender,
            receiver=receiver,
            message=message,
            appointment=self.appointment,
            sendername=sendername
        )

    @database_sync_to_async
    def get_user_instance(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            return user
        except User.DoesNotExist:
            print("Failed to find the user")

    @database_sync_to_async
    def get_doctor_instance(self, doctor_id):
        try:
            doctor = Doctorinfo.objects.get(id=doctor_id)
            return doctor
        except Doctorinfo.DoesNotExist:
            print("Failed to find the doctor")
