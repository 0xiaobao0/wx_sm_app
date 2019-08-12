# coding=utf-8
__author__ = 'wangchuan'
__date__ = '2019/6/4 8:02'

import xadmin
from .models import *

class UserMessageAdmin(object):
    list_display = ['messageId', 'senderId', 'receiveId', 'messageType', 'message', 'messageRelate', 'create_time']
    search_fields = ['messageId', 'senderId', 'receiveId', 'messageType', 'message', 'messageRelate', 'create_time']
    list_filter = ['messageId', 'senderId', 'receiveId', 'messageType', 'message', 'messageRelate', 'create_time']
    ordering = ['-create_time']




xadmin.site.register(UserMessage, UserMessageAdmin)
