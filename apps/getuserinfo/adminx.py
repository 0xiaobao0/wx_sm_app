# coding=utf-8
__author__ = 'wangchuan'
__date__ = '2019/6/3 21:24'

import xadmin
from .models import *

class UserInfoAdmin(object):
    list_display = ['userid', 'openId', 'nickName', 'gender', 'city', 'age', 'major', 'studentId', 'regist_time']
    search_fields = ['userid', 'openId', 'nickName', 'gender', 'city', 'age', 'major', 'studentId', 'regist_time']
    list_filter = ['userid', 'nickName', 'gender', 'city', 'major', 'studentId', 'regist_time']
    ordering = ['-regist_time']
    readonly_fields = ['userid','openId']


class AdminInfoAdmin(object):
    list_display = ['userid', 'name', 'create_time']
    search_fields = ['userid', 'name', 'create_time']
    list_filter = ['userid', 'name', 'create_time']
    ordering = ['-create_time']

    # def get_form_helper(self, *args, **kwargs):
    #     self.form_obj.fields['userid'].queryset = UserInfo.objects.filter('openId')  # 将想要的字段过滤出来
    #     return super(AdminInfoAdmin, self).get_form_helper(*args, **kwargs)



xadmin.site.register(UserInfo, UserInfoAdmin)
xadmin.site.register(AdminInfo, AdminInfoAdmin)