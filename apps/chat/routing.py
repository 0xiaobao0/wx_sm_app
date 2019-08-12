# coding=utf-8
from django.urls import path

from . import consumers

__author__ = 'wangchuan'
__date__ = '2019/5/15 8:53'

websocket_urlpatterns = [
    # path('ws/chat/<str:room_name>/', consumers.ChatConsumer),
    # path('ws/like/', consumers.Like),
    path('ws/', consumers.UserConnect)

]