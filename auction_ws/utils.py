from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def broadcast_auction_update(auction_id, data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"auction_{auction_id}",
        {
            "type": "auction_update",
            "data": data,
        }
    )
