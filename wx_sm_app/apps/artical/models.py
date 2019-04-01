from __future__ import unicode_literals
from django.db import models
from getuserinfo.models import UserInfo
# Create your models here.
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
    comment_type = models.CharField(verbose_name=u'评论类型', max_length=10, default=u'对文章')
    sender = models.ForeignKey(UserInfo, verbose_name=u'发送者', default=u"", blank=True, null=True, on_delete=models.CASCADE)
    comment_artical_id = models.ForeignKey(DeclareProfile, verbose_name=u'评论的文章id', on_delete=models.CASCADE)
    comment_imgurl= models.CharField(max_length=100, verbose_name=u'评论中的图片url', default=u"", blank=True, null=True)
    comment_content = models.CharField(max_length=5000, verbose_name=u'评论内容', default=u"", blank=True, null=True)
    create_time = models.DateTimeField(verbose_name=u'评论提交时间', auto_now_add=True)

    class Meta:
        verbose_name = u"对文章的评论"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.sender.nickName

class CommentCommentProfile(models.Model):
    comment_id = models.AutoField(verbose_name=u'评论id', primary_key=True)
    comment_type = models.CharField(verbose_name=u'评论类型', max_length=10, default=u'对评论')
    sender = models.ForeignKey(UserInfo, verbose_name=u'发送者', default=u"", blank=True, null=True, on_delete=models.CASCADE)
    comment_comment_id = models.ForeignKey(ArticalCommentProfile, verbose_name=u'评论的评论id', on_delete=models.CASCADE)
    comment_imgurl= models.CharField(max_length=100, verbose_name=u'评论中的图片url', default=u"", blank=True, null=True)
    comment_content = models.CharField(max_length=5000, verbose_name=u'评论内容', default=u"", blank=True, null=True)
    create_time = models.DateTimeField(verbose_name=u'评论提交时间', auto_now_add=True)

    class Meta:
        verbose_name = u"对评论的评论"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.sender.nickName