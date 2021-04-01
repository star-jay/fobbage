from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()


def session_updated(session_id):
    # send to channel_layer
    async_to_sync(channel_layer.group_send)(
        f"session_{session_id}",
        {
            "type": "session_message",
            "session_id": session_id,
        },
    )
