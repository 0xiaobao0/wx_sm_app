from __future__ import unicode_literals
from getuserinfo.models import UserInfo
from django.db import models

# Create your models here.
class UserMessage(models.Model):
    messageId = models.AutoField(verbose_name=u"消息id", primary_key=True)
    senderId = models.ForeignKey(UserInfo, verbose_name=u"发送者id", related_name='sender', default=u"", blank=True, null=True, on_delete=None)
    receiveId = models.ForeignKey(UserInfo,verbose_name=u"接收者id", related_name='receiver', default=u"", blank=True, null=True, on_delete=None)
    messageType = models.CharField(verbose_name=u'消息类型', max_length=15, default=None, blank=True, null=True)
    message = models.CharField(verbose_name=u'消息主体', max_length=2000,default=u"", blank=True, null=True)
    messageRelate = models.CharField(max_length=5000, verbose_name=u'消息涉及对象', default=u"", blank=True, null=True)
    create_time = models.DateTimeField(verbose_name=u'提交时间', auto_now_add=True)

    class Meta:
        verbose_name = u"消息表"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.messageId
