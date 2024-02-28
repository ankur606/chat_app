from . import consumers
from django.urls import path

websocket_urlpatterns = [
    
    path('ws/sc/<str:groupkaname>/', consumers.MySyncConsumer.as_asgi()),
    path('ws/ac/<str:groupkaname>/', consumers.MyAsyncConsumer.as_asgi()),
    
]
