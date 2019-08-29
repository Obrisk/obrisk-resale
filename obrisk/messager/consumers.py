import json
from slugify import slugify
from channels.generic.websocket import AsyncWebsocketConsumer


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
            username = slugify(self.scope['user'].username)
            # Accept the connection
            await self.channel_layer.group_add(f"{username}", self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        username = slugify(self.scope['user'].username)
        """Consumer implementation to leave behind the group at the moment the
        closes the connection."""
        await self.channel_layer.group_discard(f"{username}", self.channel_name)

    async def receive(self, text_data):
        """Receive method implementation to redirect any new message received
        on the websocket to broadcast to all the clients."""
        await self.send(text_data=json.dumps(text_data))
