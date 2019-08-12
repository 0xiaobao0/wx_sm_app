# coding=utf-8
__author__ = 'wangchuan'
__date__ = '2018/11/26 15:01'


from .models import DeclareProfile,ArticalProfile,ArticalCommentProfile
from rest_framework import serializers
from getuserinfo.models import UserInfo
from message.serializers import UserInfoSerializer
from django.core.cache import cache

class DeclareSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclareProfile
        fields = ('declareid', 'sender', 'towho', 'anonymous', 'imgurl', 'content', 'create_time')


class ArticalSerrializer(serializers.ModelSerializer):
    sender_nickname = serializers.SerializerMethodField()
    sender_avatarurl = serializers.SerializerMethodField()
    artical_fever = serializers.SerializerMethodField()
    class Meta:
        model = ArticalProfile
        fields = ('declareid', 'sender', 'sender_nickname', 'sender_avatarurl', 'title', 'artical', 'imgurl', 'tag', 'public', 'create_time', 'artical_fever')

    def get_sender_nickname(self, obj):
        return obj.sender.nickName

    def get_sender_avatarurl(self, obj):
        return obj.sender.avatarUrl

    def get_artical_fever(self, obj):
        key = '{}+'.format(obj.declareid)
        artical_fever = cache.get(key)
        if(artical_fever == None):
            artical_fever = 0
        return artical_fever



class CommentSerrializer(serializers.ModelSerializer):
    sender_info = serializers.SerializerMethodField()
    class Meta:
        model = ArticalCommentProfile
        fields = ('comment_id', 'belong_to', 'comment_type', 'sender', 'content', 'sender_info', 'comment_to_obj', 'create_time')

    def get_sender_info(self, obj):
        senderId = obj.sender_id
        sender_info = UserInfo.objects.filter(userid=senderId).first()
        return UserInfoSerializer(sender_info, many=False).data

