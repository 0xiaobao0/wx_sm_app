# coding=utf-8
from django import forms
from .models import *
__author__ = 'wangchuan'
__date__ = '2019/1/22 11:39'

class TopicForm(forms.Form):
    title = forms.CharField(required=True, error_messages={'required': u'请输入话题标题'})
    content = forms.CharField(required=True, error_messages={'required': u'请输入话题内容'})
    start_time = forms.CharField(required=True, error_messages={'required': u'请输入话题开始时间'})
    end_time = forms.CharField(required=True, error_messages={'required': u'请输入话题结束时间'})

class TopicModelForm(forms.ModelForm):
    class Meta:
        model = TopicProfile
        fields = '__all__'
        exclude = ['create_time']

class ArticalForm(forms.Form):
    sender = forms.IntegerField(required=True)
    title = forms.CharField(max_length=15, required=False)
    artical = forms.CharField(max_length=1000 ,required=True, error_messages={'required': u'请输入文章正文'})
    imgurl = forms.CharField(required=False)
    # tag = forms.CharField(max_length=20, required=True, error_messages={'required': u'请输入文章标签'})
    # public = forms.IntegerField(max_value=1, required=True, error_messages={'required': u'请选择是否匿名'})


class ArticalModelForm(forms.ModelForm):
    class Meta:
        model = ArticalProfile
        fields = '__all__'
        exclude = ['create_time']

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
    belong_to = forms.IntegerField(required=True, error_messages={'required': u'请添加评论归属的文章对象'})
    comment_type = forms.IntegerField(required=True, error_messages={'required': u'请添加评论类型'})
    sender = forms.IntegerField(required=True)
    content = forms.CharField(required=True)
    comment_to_obj = forms.IntegerField(required=True)


class ArticalCommentModelForm(forms.ModelForm):
    class Meta:
        model = ArticalCommentProfile
        fields = '__all__'
        exclude = ['create_time']
