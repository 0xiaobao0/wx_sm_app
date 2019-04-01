# coding=utf-8
from __future__ import unicode_literals
from django.db import models

# Create your models here.
class UserInfo(models.Model):
    userid = models.AutoField(verbose_name=u"用户id", primary_key=True)
    openId = models.CharField(verbose_name=u"用户openid",  max_length=100, default=u"")
    nickName = models.CharField(verbose_name=u"用户昵称", max_length=50, default=u"", blank=True, null=True)
    gender = models.IntegerField(choices=((0, u"未知"), (1, u"男"), (2, u"女")), default=0, blank=True, null=True)
    city =  models.CharField(verbose_name=u"所在城市", max_length=50, default=u"", blank=True, null=True)
    avatarUrl = models.CharField(verbose_name=u"头像", max_length=500, default=u"", blank=True, null=True)
    regist_time = models.DateTimeField(verbose_name=u'注册时间', auto_now_add=True)

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.nickName

