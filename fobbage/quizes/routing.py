from django.conf.urls import url
from fobbage.quizes import consumers


websocket_urlpatterns = [
    url(r'^ws/quiz/(?P<quiz_id>[^/]+)/$', consumers.ChatConsumer),
]
