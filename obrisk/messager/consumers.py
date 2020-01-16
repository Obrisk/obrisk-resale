import json

from slugify import slugify
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async	
from django.core.cache import cache	
from django.core.cache.backends.base import DEFAULT_TIMEOUT	
from config.settings.base import SESSION_COOKIE_AGE
from asgiref.sync import sync_to_async

 
from obrisk.users.models import User


class MessagerConsumer(AsyncWebsocketConsumer):
    """Consumer to manage WebSocket connections for the Messager app. """
    
    async def connect(self):
        """Consumer Connect implementation, to validate user status and prevent
        non authenticated user to take advante from the connection."""
        if self.scope["user"].is_anonymous:
            # Reject the connection
            await self.close()

        else:
            user = self.scope['user'].username
            await self.update_user_status_to_online(user)
            username = slugify(self.scope['user'].username)
            # Accept the connection
            
            await self.channel_layer.group_add(f"{username}", self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        user = self.scope['user'].username
        username = slugify(self.scope['user'].username)
        """Consumer implementation to leave behind the group at the moment the
        closes the connection."""
        await self.channel_layer.group_discard(f"{username}", self.channel_name)
        await self.update_user_status_to_offline(user)

    async def receive(self, text_data):
        """Receive method implementation to redirect any new message received
        on the websocket to broadcast to all the clients."""
        await self.send(text_data=json.dumps(text_data))


    @database_sync_to_async
    def update_user_status_to_online(self, user):
        """
        checks and updates the current status if is offline update the status to online //
        storing the current user to redis key is his id and value is none then later being updated when sending the msg
        """
        return User.objects.filter(username=user).update(status=1)
        

    @database_sync_to_async
    def update_user_status_to_offline(self, user):
        #in the future users logged in with more than one device or browsers at th same time should be handled
        """checks and updates the current status if is online update the status to offline and remove the key from redis dictionery
        """
        return User.objects.filter(username=user).update(status=0)
