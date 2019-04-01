# coding=utf-8
from django import forms
from .models import *
__author__ = 'wangchuan'
__date__ = '2019/1/22 11:39'

class DeclareForm(forms.Form):
    sender = forms.IntegerField(required=True)
    towho = forms.CharField(max_length=40 ,required=True, error_messages={'required': u'请输入表白对象'})
    anonymous = forms.IntegerField(max_value=1, required=True, error_messages={'required': u'请选择是否匿名'})
    content = forms.CharField(max_length=4000, required=True, error_messages={'required': u'内容不能为空', 'max_length': u'超出最大长度'})
    imgurl = forms.CharField(required=False)

class DeclareModelForm(forms.ModelForm):
    class Meta:
        model = DeclareProfile
        fields = '__all__'
        exclude = ['create_time']

class ArticalCommentForm(forms.Form):
    sender = forms.IntegerField(required=True)
    comment_artical_id = forms.IntegerField(required=True, error_messages={'required': u'请选择评论对象'})
    comment_imgurl = forms.CharField(required=False)
    comment_content = forms.CharField(max_length=4000, required=True, error_messages={'required': u'内容不能为空', 'max_length': u'超出最大长度'})

class CommentCommentForm(forms.Form):
    sender = forms.IntegerField(required=True)
    comment_comment_id = forms.IntegerField(required=True, error_messages={'required': u'请选择评论对象'})
    comment_imgurl = forms.CharField(required=False)
    comment_content = forms.CharField(max_length=4000, required=True, error_messages={'required': u'内容不能为空', 'max_length': u'超出最大长度'})

class ArticalCommentModelForm(forms.ModelForm):
    class Meta:
        model = ArticalCommentProfile
        fields = '__all__'
        exclude = ['create_time']

class CommentCommentModelForm(forms.ModelForm):
    class Meta:
        model = CommentCommentProfile
        fields = '__all__'
        exclude = ['create_time']