import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from slugify import slugify

from obrisk.users.models import User
from obrisk.messager.models import Conversation, Message


class MessagerConsumer(AsyncWebsocketConsumer):
    """Consumer to manage WebSocket connections for the Messager app.
    """
    async def connect(self, **kwargs):
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
            
    async def disconnect(self, close_code, **kwargs):
        user = self.scope['user'].username

        username = slugify(user)
        """Consumer implementation to leave behind the group at the moment the
        closes the connection."""
        await self.channel_layer.group_discard(f"{username}", self.channel_name)
        

    async def receive(self, text_data):
        """Receive method implementation to redirect any new message received
        on the websocket to broadcast to all the clients."""
        await self.send(text_data=json.dumps(text_data))

    