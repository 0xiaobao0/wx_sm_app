# coding=utf-8
__author__ = 'wangchuan'
__date__ = '2018/11/26 15:01'

from .models import UserMessage
from rest_framework import serializers
from getuserinfo.models import UserInfo

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('userid', 'nickName', 'gender', 'city', 'avatarUrl')

class UserMessageSerrializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    class Meta:
        model = UserMessage
        fields = ('messageId', 'messageType', 'message', 'messageRelate', 'create_time', 'sender')

    def get_sender(self, obj):
        senderid = obj.senderId_id
        userinfo = UserInfo.objects.filter(userid=senderid).first()
        return UserInfoSerializer(userinfo, many=False).data


