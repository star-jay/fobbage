from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()


def quiz_updated(quiz_id):
    # send to channel_layer
    async_to_sync(channel_layer.group_send)(
        "quiz_{}".format(quiz_id),
        {
            "type": "quiz.message",
            "quiz_id": quiz_id,
        },
    )
