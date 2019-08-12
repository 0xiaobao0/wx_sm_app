# coding=utf-8
from __future__ import unicode_literals
from django.db import models

class Openid_Session(models.Model):
    openId = models.CharField(verbose_name=u"openid",  max_length=100, primary_key=True)
    session_key = models.CharField(verbose_name=u"session_key", max_length=100, default=u"", blank=True, null=True)


    class Meta:
        verbose_name = u"openid和session_key"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.openId
