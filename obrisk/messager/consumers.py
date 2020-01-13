import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import get_object_or_404

from slugify import slugify

from obrisk.users.models import User


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
            second_user = get_object_or_404(User, username=kwargs.get("username"))
            
            user = self.scope['user'].username
            username = slugify(user, second_user)
            # Accept the connection
            await self.channel_layer.group_add(f"{username}", self.channel_name)
            await self.accept()
            await self.is_chatting(user, second_user)
            
    async def disconnect(self, close_code, **kwargs):
        user = self.scope['user'].username
        username = slugify(user)
        second_user = get_object_or_404(User, username=kwargs.get("username"))

        """Consumer implementation to leave behind the group at the moment the
        closes the connection."""
        await self.channel_layer.group_discard(f"{username}", self.channel_name)
        await self.is_not_chatting(user, second_user)
        

    async def receive(self, text_data):
        """Receive method implementation to redirect any new message received
        on the websocket to broadcast to all the clients."""
        await self.send(text_data=json.dumps(text_data))

    @database_sync_to_async
    def is_chatting(self, user, second_user):
        """
        checks and updates the user if is chatting or not 
        """
        first_user = User.objects.filter(username=user)
        value = "{}.{}".format(*sorted([first_user.pk, second_user.pk]))
        cache.set(f'joint_chat_{first_user.pk}', value)

        return User.objects.filter(username=user).update(is_chatting=1)

        
    @database_sync_to_async
    def is_not_chatting(self, user, second_user):
        """
        checks and updates the user if is chatting or not 
        """
        first_user = User.objects.filter(username=user)
        key = "{}.{}".format(*sorted([first_user.pk, second_user.pk]))
        data = cache.get(f'joint_chat_{first_user.pk}', key)
        data.clear()

        return User.objects.filter(username=user).update(is_chatting=0)


