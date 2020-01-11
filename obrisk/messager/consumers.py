import json
from slugify import slugify
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import F
from channels.db import database_sync_to_async
from obrisk.users.models import User
class MessagerConsumer(AsyncWebsocketConsumer):
    """Consumer to manage WebSocket connections for the Messager app.
    """
    async def connect(self):
        """Consumer Connect implementation, to validate user status and prevent
        non authenticated user to take advante from the connection."""
        if self.scope["user"].is_anonymous:
            # Reject the connection
            await self.close()

        else:
            user = self.scope['user'].username
            username = slugify(user)
            # Accept the connection
            await self.channel_layer.group_add(f"{username}", self.channel_name)
            await self.accept()
            await self.is_chatting(user)
            
    async def disconnect(self, close_code):
        user = self.scope['user'].username
        username = slugify(user)
        """Consumer implementation to leave behind the group at the moment the
        closes the connection."""
        await self.channel_layer.group_discard(f"{username}", self.channel_name)
        await self.is_not_chatting(user)
        

    async def receive(self, text_data):
        """Receive method implementation to redirect any new message received
        on the websocket to broadcast to all the clients."""
        await self.send(text_data=json.dumps(text_data))

    @database_sync_to_async
    def is_chatting(self, username):
        """
        checks and updates the user if is chatting or not 
        """
        chatting = User.objects.filter(username=username).update(is_chatting=1)

        # if chatting > 0:
        #     not_chatting = chatting
        #     return not_chatting
        # elif chatting < 1:
        #     is_chatting = chatting.update(is_chatting == 1)
        return chatting

    @database_sync_to_async
    def is_not_chatting(self, username):
        """
        checks and updates the user if is chatting or not 
        """
        not_chatting = User.objects.filter(username=username).update(is_chatting=0)
        return not_chatting
