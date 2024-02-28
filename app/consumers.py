import json
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
import time
import asyncio

from asgiref.sync import async_to_sync
from .models import Chat, Group
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()
class MySyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        print("WebSocket connected...")
        print("Channel Layers ", self.channel_layer)
        print("Channel Name ", self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['groupkaname']
        print(self.group_name)
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        print("Message Recevied....", event)
        data =  json.loads(event['text'])
        print("Data", data['msg'], type(data))
        # Find Group Model Object 
        group = Group.objects.get(name = self.group_name)
        send_user = User.objects.get(id=self.scope['user'].id)
        print("Sender", send_user)
        if self.scope['user'].is_authenticated:
        # Create new Chat object
            chat = Chat(
                content = data['msg'],
                group = group,
                send_msg_friend = send_user.id
        
            )
            chat.save()
            data['user'] = self.scope['user'].username
            print("Data nUSer", data)
            async_to_sync(self.channel_layer.group_send)(self.group_name, {
                'type': 'chat.message',
                'message': json.dumps(data)
            })
        else:
            self.send({
                'type':'websocket.send',
                'text': json.dumps({'msg':"Login Required", 'user':"Guest"})
            })
    def chat_message(self, event):
        print("Event Message", event)
        self.send({
            'type': 'websocket.send',
            'text': event['message']
        })

    def websocket_disconnect(self, event):
        print("WebSocket Disconnected.....")
        print("Channel Layers ", self.channel_layer)
        print("Channel Name ", self.channel_name)
        
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
        raise StopConsumer()

class MyAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("WebSocket connected...")
        print("Channel Layers ", self.channel_layer)
        print("Channel Name ", self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['groupkaname']
        print("ANkur", self.group_name)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print("Message Received...", event)
        data = json.loads(event['text'])

        group = await database_sync_to_async(Group.objects.get)(name=self.group_name)

        # Check if the user is authenticated
        if self.scope['user'].is_authenticated:
            # Create new Chat object and save it
            chat = Chat(
                content=data['msg'],
                group=group
            )

            try:
                await database_sync_to_async(chat.save)()
            except Exception as e:
                print(f"Error while saving chat message: {str(e)}")
            data['user'] = self.scope['user'].username

            # Send chat message to all users in the group
            await self.channel_layer.group_send(self.group_name, {
                'type': 'chat.message',
                'message': json.dumps(data)
            })
        else:
            # Send a message informing the user to login
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps({'msg': "Login Required", 'user': "Guest"})
            })

    async def chat_message(self, event):
        print("Event Message", event)
        await self.send({
            'type': 'websocket.send',
            'text': event['message']
        })


    async def websocket_disconnect(self, event):
        print("WebSocket Disconnected.....")
        print("Channel Layers ", self.channel_layer)
        print("Channel Name ", self.channel_name)
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        raise StopConsumer()