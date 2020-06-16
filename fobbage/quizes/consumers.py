# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, SyncConsumer
import json

from .models import Bluff, Quiz


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.quiz_id = self.scope['url_route']['kwargs']['quiz_id']
        self.room_group_name = 'quiz_%s' % self.quiz_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        # accept websocket
        self.accept()
        # report user has joined
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'quiz_message',
                'message': 'user joined: {}'.format(self.get_username()),
                'user': self.get_username(),
            }
        )

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def get_username(self):
        self.user = self.scope["user"]
        self.quiz = Quiz.objects.get(id=self.quiz_id)
        if self.user.is_authenticated:
            return self.user.username
        else:
            return 'anonymous'

    # Receive message from WebSocket
    def receive(self, text_data):
        user = self.get_username()

        text_data_json = json.loads(text_data)
        if 'message' in text_data_json:
            message = text_data_json['message']

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': user,
                }
            )

        elif 'answer' in text_data_json:
            answer = Bluff.objects.create(
                player=self.user,
                question=self.quiz.active_question,
                text=text_data_json['answer']
            )

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': answer.text,
                    'user': user,
                }
            )

    # Receive message from room group
    def quiz_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps(event))

    # Receive message from room group
    def user_joined(self):
        user = self.get_username()

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': 'user joined: {}'.format(user)
        }))


class EchoConsumer(SyncConsumer):
    def test(self, event):
        print(event['message'])
