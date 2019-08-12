# coding=utf-8
__author__ = 'wangchuan'
__date__ = '2019/5/15 8:54'

from wx_sm_app.utils import decode_jwt
import datetime
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from getuserinfo.models import UserInfo



class UserConnect(WebsocketConsumer):
    def connect(self):
        token = self.scope['subprotocols'][0]
        result = decode_jwt(token)
        if (result['state'] == True):
            Token = result['Token']
            openId = Token['openid']
            userId = UserInfo.objects.filter(openId=openId).first().userid
            self.Group = 'wx_user'
            self.name = str(userId)
            print('用户'+self.name+'已建立连接')
            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.name,
                self.channel_name
            )
            async_to_sync(self.channel_layer.group_add)(
                self.Group,
                self.channel_name
            )
            self.accept(subprotocol=token)


    def disconnect(self, close_code):
        # Leave room group
        print('用户' + self.name + '正在断开连接')
        async_to_sync(self.channel_layer.group_discard)(
            self.name,
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_discard)(
            self.Group,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        message = text_data
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')

        if not message:
            return
        # if not self.userId:
        #     return

        print(message)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.Group,
            {
                'type': 'push_message',
                'message_type': 'reply',
                'message': message,
                'now_time': now_time
            }
        )
        # async_to_sync(self.channel_layer.group_send)(
        #     self.name,
        #     {
        #         'type': 'push_message',
        #         'message': message,
        #         'now_time': now_time
        #     }
        # )

    # Receive message from room group
    def user_message(self, event):
        messageId = event['messageId']
        message_type = event['message_type']
        message = event['message']
        messageRelate = event['messageRelate']
        create_time = datetime.datetime.now().strftime('%Y-%m-%d')
        senderId = event['senderId']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'messageId': messageId,
            'message_type': message_type,
            'messageObj': message,
            'messageRelate': messageRelate,
            'create_time': create_time,
            'sender': senderId,
        }))

    def push_message(self, event):
        message_type = event['message_type']
        message = event['message']
        now_time = event['now_time']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message_type': message_type,
            'message': message,
            'now_time': now_time,
        }))

