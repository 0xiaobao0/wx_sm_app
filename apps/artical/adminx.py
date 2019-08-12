# coding=utf-8
__author__ = 'wangchuan'
__date__ = '2019/6/3 23:53'

import xadmin
from .models import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import datetime
from message.models import UserMessage
from django.forms.models import model_to_dict
from xadmin.sites import site
from xadmin.views.edit import ModelFormAdminView


class TopicPostAdmin(object):
    list_display = ['title', 'content', 'start_time', 'end_time', 'create_time']
    search_fields = ['title', 'content', 'start_time', 'end_time', 'create_time']
    list_filter = ['title', 'content', 'start_time', 'end_time', 'create_time']
    ordering = ['-create_time']
    # list_editable = ['title', 'content', 'start_time', 'end_time', 'create_time']

    def save_forms(self):
        # print(self.form_obj.changed_data)
        self.new_obj = self.form_obj.save(commit=False)
        channel_layer = get_channel_layer()
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        # Send message to room group
        async_to_sync(channel_layer.group_send)(
            'wx_user',
            {
                'type': 'push_message',
                'message_type': 'topic',
                'message': self.form_obj.cleaned_data,
                'now_time': now_time
            }
        )

    # def queryset(self):
    #     # 重载queryset方法，来过滤出我们想要的数据的
    #     qs = super(TopicPostAdmin, self).queryset()
    #     # 只显示xx字段
    #     qs = qs.filter(title='毕业季')
    #     return qs


    # def post(self, request, *args, **kwargs):
    #     print('haha')
    #     return super().post(request, args, kwargs)




class ArticalProfileAdmin(object):
    list_display = ['declareid', 'sender', 'title', 'artical', 'tag', 'adopt', 'create_time']
    search_fields = ['declareid', 'sender', 'title', 'artical', 'tag', 'adopt', 'create_time']
    list_filter = ['declareid', 'sender', 'title', 'artical', 'tag', 'adopt', 'create_time']
    ordering = ['-create_time']
    # list_editable = ['adopt']

    def save_forms(self):
        # print(self.form_obj.changed_data)
        user = self.form_obj.cleaned_data['sender'].userid
        self.new_obj = self.form_obj.save(commit=False)
        # Send message to room group
        if(self.form_obj.cleaned_data['adopt'] == 1):
            channel_layer = get_channel_layer()
            now_time = datetime.datetime.now().strftime('%Y-%m-%d')
            async_to_sync(channel_layer.group_send)(
                str(user),
                {
                    'type': 'push_message',
                    'message_type': 'artical_pass',
                    'message': {
                        'artical': self.form_obj.cleaned_data['artical']
                    },
                    'now_time': now_time
                }
            )

class ArticalCommentProfileAdmin(object):
    list_display = ['comment_id', 'belong_to', 'comment_type', 'sender', 'content', 'comment_to_obj', 'adopt', 'create_time']
    search_fields = ['comment_id', 'belong_to', 'comment_type', 'sender', 'content', 'comment_to_obj', 'adopt', 'create_time']
    list_filter = ['comment_id', 'belong_to', 'comment_type', 'sender', 'content', 'comment_to_obj', 'adopt', 'create_time']
    ordering = ['-create_time']
    # list_editable = ['adopt']

    def save_forms(self):
        # print(self.form_obj.changed_data)
        sender = self.form_obj.cleaned_data['sender'].userid
        receiver = self.form_obj.cleaned_data['belong_to'].sender.userid
        self.new_obj = self.form_obj.save(commit=False)
        # Send message to room group
        if(self.form_obj.cleaned_data['adopt'] == 1):
            channel_layer = get_channel_layer()
            now_time = datetime.datetime.now().strftime('%Y-%m-%d')
            async_to_sync(channel_layer.group_send)(
                str(sender),
                {
                    'type': 'push_message',
                    'message_type': 'comment_pass',
                    'message': {
                        'artical': self.form_obj.cleaned_data['content']
                    },
                    'now_time': now_time
                }
            )

            message = UserMessage(senderId_id=sender, receiveId_id=receiver, messageType='comment_message',
                                  message='收到一条评论',
                                  messageRelate=self.form_obj.cleaned_data['belong_to'].sender)
            message.save()
            message_dict = model_to_dict(UserMessage.objects.filter(receiveId_id=receiver).last())
            message_dict['type'] = 'user_message'
            message_dict['message_type'] = 'comment_message'
            async_to_sync(channel_layer.group_send)(
                str(receiver),
                message_dict
            )




xadmin.site.register(TopicProfile, TopicPostAdmin)
xadmin.site.register(ArticalProfile, ArticalProfileAdmin)
xadmin.site.register(ArticalCommentProfile, ArticalCommentProfileAdmin)