import json
import re
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)


def sanitize_group_name(name: str) -> str:
    sanitized = re.sub(r'[^a-zA-Z0-9._-]', '_', name)
    # Group name must be < 100; allow prefix 'notifications_' (14 chars)
    max_len = 99 - len('notifications_')
    if len(sanitized) > max_len:
        sanitized = sanitized[:max_len]
    return sanitized


class NotificationsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_role = self.scope['url_route']['kwargs'].get('user_role', 'guest')
        self.user_role = sanitize_group_name(self.user_role.lower())
        self.group_name = f'notifications_{self.user_role}'

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        logger.info(f"Notifications WebSocket connected: role={self.user_role}")

        # Optional hello event
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'title': 'Connected',
            'message': f'Subscribed to {self.user_role} notifications',
            'timestamp': None,
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        logger.info(f"Notifications WebSocket disconnected: role={self.user_role} code={close_code}")

    async def receive(self, text_data):
        # This consumer is broadcast-only; ignore incoming messages
        logger.debug(f"Client message ignored for role={self.user_role}: {text_data}")

    async def notification(self, event):
        # Forward notification events to client
        await self.send(text_data=json.dumps(event))



