import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.user_group = None   # hởi tạo mặc định

        if self.user.is_anonymous:
            await self.close()
        else:
            self.user_group = f"user_{self.user.id}"   # Gán group theo user id

            # Thêm vào group
            await self.channel_layer.group_add(
                self.user_group,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        # Chỉ discard nếu đã gán group
        if self.user_group:
            await self.channel_layer.group_discard(self.user_group, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.send(text_data=json.dumps({
            "message": f"Server received: {data}"
        }))

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            "notification": event["notification"]
        }))
