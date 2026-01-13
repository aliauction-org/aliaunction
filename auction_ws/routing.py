from channels.generic.websocket import AsyncWebsocketConsumer
import json

class AuctionUpdatesConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.auction_id = self.scope["url_route"]["kwargs"]["auction_id"]
        self.group_name = f"auction_{self.auction_id}"

        # Accept connection
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # 🔒 BLOCK ALL CLIENT MESSAGES
    async def receive(self, text_data=None, bytes_data=None):
        # Client is NOT allowed to send anything
        await self.close(code=4001)

    # ✅ SERVER → CLIENT ONLY
    async def auction_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))
