import json
from slugify import slugify
from channels.generic.websocket import AsyncWebsocketConsumer
from obrisk.users.models import User
from django.db.models import F
from channels.db import database_sync_to_async

class NotificationsConsumer(AsyncWebsocketConsumer):
    """Consumer to manage WebSocket connections for the Notification app,
    called when the websocket is handshaking as part of initial connection.
    """
    async def connect(self):
        """Consumer Connect implementation, to validate user status and prevent
        non authenticated user to take advante from the connection."""
        if self.scope["user"].is_anonymous:
            # Reject the connection
            await self.close()

        else:
            username = self.scope['user'].username
            await self.update_user_status_to_online(username)
            
            # Accept the connection
            await self.channel_layer.group_add(
                'notifications', self.channel_name)            
            await self.accept()
            
    async def disconnect(self, close_code):
        """Consumer implementation to leave behind the group at the moment the
        closes the connection."""
        username = self.scope['user'].username
        await self.update_user_status_to_offline(username)      
        await self.channel_layer.group_discard(
           'notifications', self.channel_name)


    async def receive(self, text_data):
        """Receive method implementation to redirect any new message received
        on the websocket to broadcast to all the clients."""
        await self.send(text_data=json.dumps(text_data))
    
    @database_sync_to_async
    def update_user_status_to_online(self, username):
        """
        checks and updates the current status if is offline update the status to online 
        """
        return User.objects.filter(username=username).update(status=1)
        # current_status = current_status.status
        # if current_status != 1:
        #     return current_status
        # else:    
        #     return current_status


    @database_sync_to_async
    def update_user_status_to_offline(self, username):
        #in the future users logged in with more than one device or browsers at th same time should be handled
        """checks and updates the current status if is online update the status to offline """

        
        return User.objects.filter(username=username).update(status=0)
