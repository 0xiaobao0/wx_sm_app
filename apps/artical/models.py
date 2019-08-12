from __future__ import unicode_literals
from django.db import models
from getuserinfo.models import UserInfo
# Create your models here.

class TopicProfile(models.Model):
    title = models.CharField(verbose_name=u'话题标题', max_length=50, default=u"", blank=True, null=True)
    content = models.CharField(verbose_name=u'话题内容', default=u"",max_length=50, blank=True, null=True)
    start_time = models.CharField(verbose_name=u'话题开始时间', default=u"", max_length=50,  blank=True, null=True)
    end_time = models.CharField(verbose_name=u'话题结束时间', default=u"", max_length=50, blank=True, null=True)
    create_time = models.DateTimeField(verbose_name=u'提交时间', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u"话题"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title

class ArticalProfile(models.Model):
    declareid = models.AutoField(verbose_name=u'文章内容id', primary_key=True)
    sender = models.ForeignKey(UserInfo, verbose_name=u'发送者', default=u"", blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=15, verbose_name=u'文章标题', default=u"", blank=True, null=True)
    artical = models.CharField(max_length=1000, verbose_name=u'内容', default=u"", blank=True, null=True)
    imgurl = models.CharField(max_length=1500, verbose_name=u'图片url', default=u"", blank=True, null=True)
    tag = models.CharField(max_length=15, verbose_name=u'文章标签', default=u"", blank=True, null=True)
    public = models.IntegerField(verbose_name=u'是否匿名', choices=((1, u"匿名"), (0, "不匿名")), default=0, blank=True, null=True)
    adopt = models.IntegerField(choices=((0, u"未审核"), (1, u"审核通过"), (2, u"审核不通过")), default=0, blank=True, null=True)
    create_time = models.DateTimeField(verbose_name=u'提交时间', auto_now_add=True)

    def __str__(self):
        return str(self.declareid)

    class Meta:
        verbose_name = u"文章信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.sender.nickName

class DeclareProfile(models.Model):
    declareid = models.AutoField(verbose_name=u'表白内容id', primary_key=True)
    sender = models.ForeignKey(UserInfo, verbose_name=u'发送者', default=u"", blank=True, null=True, on_delete=models.CASCADE)
    towho = models.CharField(max_length=20, verbose_name=u'接受者', default=u"", blank=True, null=True)
    anonymous = models.IntegerField(verbose_name=u'是否匿名', choices=((1, u"匿名"), (0, "不匿名")), default=0, blank=True, null=True)
    imgurl= models.CharField(max_length=100, verbose_name=u'图片url', default=u"", blank=True, null=True)
    content = models.CharField(max_length=5000, verbose_name=u'内容', default=u"", blank=True, null=True)
    create_time = models.DateTimeField(verbose_name=u'提交时间', auto_now_add=True)

    class Meta:
        verbose_name = u"表白信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.sender.nickName

class ArticalCommentProfile(models.Model):
    comment_id = models.AutoField(verbose_name=u'评论id', primary_key=True)
    belong_to = models.ForeignKey(ArticalProfile, verbose_name=u'评论归属的文章', blank=True, null=True, on_delete=None)
    comment_type = models.IntegerField(verbose_name=u'评论类型', choices=((0, u"对文章的评论"), (1, u"对评论的评论")), default=0, blank=True, null=True,)
    sender = models.ForeignKey(UserInfo, verbose_name=u'评论发送者', default=u"", blank=True, null=True, on_delete=None)
    content = models.CharField(verbose_name=u'评论内容', max_length=1000, blank=True, null=True)
    comment_to_obj = models.IntegerField(verbose_name="评论对象的id", default=u"", blank=True, null=True)
    adopt = models.IntegerField(choices=((0, u"未审核"), (1, u"审核通过"), (2, u"审核不通过")), default=0, blank=True, null=True)
    create_time = models.DateTimeField(verbose_name=u'评论提交时间', auto_now_add=True)

    def __str__(self):
        return str(self.comment_id)

    class Meta:
        verbose_name = u"文章评论"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.sender.nickName

